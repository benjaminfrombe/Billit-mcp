#!/usr/bin/env python3
"""Generate Cursor deeplink for Billit MCP with auto-update."""

import json
import base64

# Configuration for auto-updating installation
config = {
    "command": "pipx",
    "args": ["run", "--no-cache", "--spec", "billit-mcp", "python", "-m", "billit_mcp"],
    "env": {
        "BILLIT_API_KEY": "",
        "BILLIT_BASE_URL": "https://api.billit.be/v1",
        "BILLIT_PARTY_ID": "",
        "BILLIT_CONTEXT_PARTY_ID": ""
    }
}

# Convert to JSON and base64 encode
json_str = json.dumps(config, separators=(',', ':'))
encoded = base64.b64encode(json_str.encode()).decode()

# Create the deeplink URL
deeplink = f"cursor://anysphere.cursor-deeplink/mcp/install?name=billit-mcp&config={encoded}"

print("Auto-updating Cursor deeplink:")
print(deeplink)
print("\nConfiguration (decoded):")
print(json.dumps(config, indent=2))
