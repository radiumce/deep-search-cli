#!/bin/bash
# Install deep-search CLI client

set -e

INSTALL_DIR="$HOME/.local/bin"
EXECUTABLE="$INSTALL_DIR/deep-search"

echo "Installing deep-search CLI client..."

# Ensure target directory exists
mkdir -p "$INSTALL_DIR"

if [ -f "scripts/deep-search.py" ]; then
    # Local install from repo
    echo "Copying local script to $EXECUTABLE..."
    cp scripts/deep-search.py "$EXECUTABLE"
else
    # Network install
    echo "Downloading deep-search-cli from GitHub..."
    URL="https://raw.githubusercontent.com/radiumce/deep-search-cli/main/scripts/deep-search.py"
    if curl -sSLf "$URL" -o "$EXECUTABLE"; then
        echo "Successfully downloaded deep-search.py."
    else
        echo "Error: Failed to download deep-search.py from $URL"
        exit 1
    fi
fi

chmod +x "$EXECUTABLE"

echo "Installation complete!"
echo "The 'deep-search' command is now installed at: $EXECUTABLE"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "WARNING: $HOME/.local/bin is not in your PATH."
    echo "To use 'deep-search' from anywhere, please add the following line to your shell profile (e.g., ~/.bashrc or ~/.zshrc):"
    echo ""
    echo 'export PATH="$HOME/.local/bin:$PATH"'
    echo ""
    echo "After adding it, restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
fi

echo ""
echo "Run 'deep-search --help' to get started!"
