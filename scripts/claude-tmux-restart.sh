#!/usr/bin/env bash
# claude-tmux-restart.sh - Restart Claude within the same tmux session

set -euo pipefail

SESSION_NAME="claude-mcp-billit-mcp"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CURRENT_DIR=$(pwd)

echo "🤖 Claude Tmux Restart - Billit MCP"
echo "=================================="
echo ""

# Check if we're in a tmux session
if [ -z "${TMUX:-}" ]; then
    echo "❌ Not running in a tmux session!"
    echo "   Start Claude with: ./scripts/claude-tmux-start.sh"
    exit 1
fi

# Get current pane ID
PANE_ID=$(tmux display-message -p '#{pane_id}')

echo "📍 Current tmux pane: $PANE_ID"
echo "🔄 Restarting Claude in 2 seconds..."
sleep 2

# Use tmux respawn-pane to restart the command
# This kills the current process and restarts with a new command
echo "🔄 Using tmux respawn-pane to restart Claude..."

# Kill the pane process and respawn with Claude
tmux respawn-pane -t "$PANE_ID" -k "cd '$CURRENT_DIR' && claude --dangerously-skip-permissions -c"

# Wait for Claude to start up, then send the continuation message
# Use just Enter with a small delay to ensure the text is typed first
(sleep 8 && tmux send-keys -t "$PANE_ID" "Restart completed. Proceed autonomously." && sleep 0.5 && tmux send-keys -t "$PANE_ID" Enter) &

echo "✅ Restart command sent!"
echo "   Claude will restart in the same terminal pane"
echo "   Auto-continuation message will be sent in 8 seconds..."
echo "   Billit MCP tools should be available after restart"