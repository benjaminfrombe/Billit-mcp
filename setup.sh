#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting Billit MCP server environment setup..."

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv could not be found. Please install it first."
    echo "See: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# 1. Verify project configuration
if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found. Please ensure you're in the correct directory."
    exit 1
else
    echo "Project configuration found."
fi

# 2. Install dependencies from the committed lock file
echo "Installing dependencies..."
uv sync --locked

# 3. Create the .env file from the template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# .env
# Billit API credentials.
BILLIT_API_KEY="YOUR_API_KEY"
BILLIT_BASE_URL="https://api.billit.be/v1"
BILLIT_PARTY_ID="YOUR_COMPANY_OR_PARTY_ID"
BILLIT_CONTEXT_PARTY_ID=""

# Optional FastAPI adapter settings.
MCP_SERVER_PORT=8000
LOG_LEVEL="INFO"

# Shared Billit API rate limiter.
RATE_LIMIT_PER_MINUTE=60
EOL
else
    echo ".env file already exists, skipping creation."
fi

echo ""
echo "Setup complete."
echo "Next steps:"
if [ -f .env ]; then
    echo "1. Fill in your API key and Party ID in the .env file."
else
    echo "1. .env file already configured."
fi
echo "2. Run the MCP server with: uv run billit-mcp"
echo "3. For the legacy FastAPI adapter, run: uv run uvicorn server:app --reload"
