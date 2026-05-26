#!/bin/bash

# Script to run live integration tests for Billit MCP Server

set -e

echo "🧪 Billit MCP Server - Live Integration Tests"
echo "============================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your Billit API credentials."
    echo "See .env.example for the required format."
    exit 1
fi

# Check if credentials are set
source .env
if [ -z "$BILLIT_API_KEY" ]; then
    echo "❌ Error: BILLIT_API_KEY not set in .env file!"
    exit 1
fi

if [ -z "$BILLIT_PARTY_ID" ]; then
    echo "❌ Error: BILLIT_PARTY_ID not set in .env file!"
    exit 1
fi

echo "✅ Credentials found"
echo "📍 API URL: $BILLIT_BASE_URL"
echo "🏢 Party ID: $BILLIT_PARTY_ID"
echo ""
echo "⚠️  WARNING: These tests will connect to the live API!"
echo "⚠️  Ensure you're using SANDBOX credentials!"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Test run cancelled."
    exit 0
fi

echo ""
echo "🚀 Starting live tests..."
echo ""

# Run the tests
poetry run pytest tests/test_live_integration.py -v --live -s

echo ""
echo "✅ Live tests completed!"