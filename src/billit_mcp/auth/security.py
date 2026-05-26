"""Security primitives for hosted Billit MCP mode."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

import jwt
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

if TYPE_CHECKING:
    from billit_mcp.hosted_config import HostedSettings


def sha256_text(value: str) -> str:
    """Return a hex SHA-256 hash for a text value."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def random_token_urlsafe() -> str:
    """Return a high-entropy URL-safe token."""

    return secrets.token_urlsafe(32)


def ensure_aware_utc(value: datetime) -> datetime:
    """Normalize SQLite/Postgres datetimes to aware UTC values."""

    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def b64url_uint(value: int) -> str:
    """Return a base64url-encoded unsigned integer without padding."""

    byte_length = (value.bit_length() + 7) // 8
    raw = value.to_bytes(byte_length, "big")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def verify_pkce_s256(verifier: str, challenge: str) -> bool:
    """Verify a PKCE S256 code verifier."""

    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    computed = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return hmac.compare_digest(computed, challenge)


@dataclass
class FernetCipher:
    """Small Fernet wrapper for token encryption."""

    fernet: Fernet
    key_version: str = "v1"

    @classmethod
    def from_settings(cls, settings: HostedSettings) -> FernetCipher:
        """Build a Fernet cipher from settings, with dev fallback only."""

        key = settings.token_encryption_key
        if not key:
            if settings.environment == "production":
                raise RuntimeError("BILLIT_TOKEN_ENCRYPTION_KEY is required in production")
            digest = hashlib.sha256(b"billit-mcp-local-development-key").digest()
            key = base64.urlsafe_b64encode(digest).decode("ascii")
        return cls(Fernet(key.encode("ascii")))

    def encrypt(self, value: str) -> str:
        """Encrypt a text value."""

        return self.fernet.encrypt(value.encode("utf-8")).decode("ascii")

    def decrypt(self, value: str) -> str:
        """Decrypt a text value."""

        try:
            return self.fernet.decrypt(value.encode("ascii")).decode("utf-8")
        except InvalidToken as exc:
            raise ValueError("Unable to decrypt hosted secret") from exc


class JWTService:
    """RS256 JWT signer/verifier and JWKS provider."""

    def __init__(self, settings: HostedSettings) -> None:
        """Create a JWT service using configured or dev-generated keys."""

        if settings.jwt_private_key_pem:
            private_key = serialization.load_pem_private_key(
                settings.jwt_private_key_pem.encode("utf-8"), password=None
            )
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise RuntimeError("BILLIT_MCP_JWT_PRIVATE_KEY_PEM must be an RSA private key")
            self._private_key: rsa.RSAPrivateKey = private_key
        else:
            if settings.environment == "production":
                raise RuntimeError("BILLIT_MCP_JWT_PRIVATE_KEY_PEM is required in production")
            self._private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.issuer = settings.issuer_url
        self.audience = settings.resource_url
        self.key_id = sha256_text(self.public_key_pem().decode("utf-8"))[:16]

    def public_key_pem(self) -> bytes:
        """Return the PEM-encoded public key."""

        return self._private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def jwks(self) -> dict[str, Any]:
        """Return public JSON Web Key Set data."""

        numbers = self._private_key.public_key().public_numbers()
        return {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "alg": "RS256",
                    "kid": self.key_id,
                    "n": b64url_uint(numbers.n),
                    "e": b64url_uint(numbers.e),
                }
            ]
        }

    def issue_access_token(
        self,
        *,
        actor_id: str,
        client_id: str,
        scopes: list[str],
        lifetime: timedelta = timedelta(minutes=30),
    ) -> tuple[str, dict[str, Any]]:
        """Issue an MCP access token and return token plus claims."""

        now = datetime.now(UTC)
        claims: dict[str, Any] = {
            "iss": self.issuer,
            "sub": actor_id,
            "aud": self.audience,
            "client_id": client_id,
            "scope": " ".join(scopes),
            "jti": random_token_urlsafe(),
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "exp": int((now + lifetime).timestamp()),
        }
        token = jwt.encode(
            claims,
            self._private_key,
            algorithm="RS256",
            headers={"kid": self.key_id},
        )
        return token, claims

    def decode(self, token: str) -> dict[str, Any]:
        """Decode and verify an MCP access token."""

        return jwt.decode(
            token,
            self.public_key_pem(),
            algorithms=["RS256"],
            issuer=self.issuer,
            audience=self.audience,
        )
