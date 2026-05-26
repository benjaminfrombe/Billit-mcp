from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    """Address model for party addresses."""

    address_type: str | None = Field(None, alias="AddressType")
    name: str | None = Field(None, alias="Name")
    street: str | None = Field(None, alias="Street")
    street_number: str | None = Field(None, alias="StreetNumber")
    box: str | None = Field(None, alias="Box")
    zipcode: str | None = Field(None, alias="Zipcode")
    city: str | None = Field(None, alias="City")
    country_code: str | None = Field(None, alias="CountryCode")

    model_config = ConfigDict(populate_by_name=True)


class Party(BaseModel):
    """Complete party model matching Billit API response structure."""

    party_id: int = Field(alias="PartyID")
    name: str = Field(alias="Name")

    # Contact information
    commercial_name: str | None = Field(None, alias="CommercialName")
    contact_first_name: str | None = Field(None, alias="ContactFirstName")
    contact_last_name: str | None = Field(None, alias="ContactLastName")
    email: str | None = Field(None, alias="Email")
    phone: str | None = Field(None, alias="Phone")
    mobile: str | None = Field(None, alias="Mobile")
    fax: str | None = Field(None, alias="Fax")

    # Business information
    vat_number: str | None = Field(None, alias="VATNumber")
    iban: str | None = Field(None, alias="IBAN")
    language: str | None = Field(None, alias="Language")
    vat_liable: bool | None = Field(None, alias="VATLiable")

    # Primary address (flat fields)
    street: str | None = Field(None, alias="Street")
    street_number: str | None = Field(None, alias="StreetNumber")
    box: str | None = Field(None, alias="Box")
    zipcode: str | None = Field(None, alias="Zipcode")
    city: str | None = Field(None, alias="City")
    country_code: str | None = Field(None, alias="CountryCode")

    # Structured addresses array
    addresses: list[Address] | None = Field(None, alias="Addresses")

    # Accounting integration
    gl_account_code: str | None = Field(None, alias="GLAccountCode")
    gl_default_expiry_offset: str | None = Field(None, alias="GLDefaultExpiryOffset")
    nr: str | None = Field(None, alias="Nr")
    external_provider_tc: str | None = Field(None, alias="ExternalProviderTC")
    external_provider_id: str | None = Field(None, alias="ExternalProviderID")

    # Party type
    party_type: str | None = Field(None, alias="PartyType")

    model_config = ConfigDict(populate_by_name=True)


class PartyCreate(BaseModel):
    name: str


class PartyUpdate(BaseModel):
    """Model for updating party (customer/supplier) information.

    All fields are optional for PATCH operations.
    Based on Billit API patchable properties documentation.

    Note: Addresses can be updated via flat fields (primary address) or
    structured Addresses array. Flat fields appear to be more reliable
    for updates via PATCH operations.
    """

    name: str | None = Field(None, alias="Name")
    commercial_name: str | None = Field(None, alias="CommercialName")
    contact_first_name: str | None = Field(None, alias="ContactFirstName")
    contact_last_name: str | None = Field(None, alias="ContactLastName")
    email: str | None = Field(None, alias="Email")
    phone: str | None = Field(None, alias="Phone")
    mobile: str | None = Field(None, alias="Mobile")
    fax: str | None = Field(None, alias="Fax")
    vat_number: str | None = Field(None, alias="VATNumber")
    iban: str | None = Field(None, alias="IBAN")
    language: str | None = Field(None, alias="Language")

    # Primary address fields (recommended for updates)
    country_code: str | None = Field(None, alias="CountryCode")
    city: str | None = Field(None, alias="City")
    street: str | None = Field(None, alias="Street")
    street_number: str | None = Field(None, alias="StreetNumber")
    zipcode: str | None = Field(None, alias="Zipcode")
    box: str | None = Field(None, alias="Box")

    # Structured addresses (may not be patchable - needs testing)
    addresses: list[Address] | None = Field(None, alias="Addresses")

    # Other fields
    vat_liable: bool | None = Field(None, alias="VATLiable")
    gl_account_code: str | None = Field(None, alias="GLAccountCode")
    gl_default_expiry_offset: str | None = Field(None, alias="GLDefaultExpiryOffset")
    nr: str | None = Field(None, alias="Nr")
    external_provider_tc: str | None = Field(None, alias="ExternalProviderTC")
    external_provider_id: str | None = Field(None, alias="ExternalProviderID")

    model_config = ConfigDict(populate_by_name=True)
