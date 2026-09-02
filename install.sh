#!/bin/bash
set -e

# install.sh - installs and packages the YouTube to MP3 desktop app
#
# Usage:
#   chmod +x install.sh
#   ./install.sh

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "==> Project directory: $PROJECT_DIR"

# --- 1. Check/install Python ---
if ! command -v python3 &> /dev/null; then
    echo "==> python3 is not installed. Installing it with apt (you'll be asked for your password)..."
    sudo apt update
    sudo apt install -y python3

    if ! command -v python3 &> /dev/null; then
        echo "ERROR: could not install python3 automatically. Install it manually and try again."
        exit 1
    fi
fi

# --- 2. Check/install other system dependencies ---
MISSING=""

python3 -c "import tkinter" 2>/dev/null || MISSING="$MISSING python3-tk"
command -v ffmpeg &> /dev/null || MISSING="$MISSING ffmpeg"
python3 -m venv --help &> /dev/null || MISSING="$MISSING python3-venv"

if [ -n "$MISSING" ]; then
    echo "==> Missing system packages:$MISSING"
    echo "==> Installing with apt (you'll be asked for your password)..."
    sudo apt update
    sudo apt install -y $MISSING
else
    echo "==> All system dependencies are already installed."
fi


# --- 3. Create the .desktop launcher with the correct absolute path ---
chmod +x dist/app_desktop
EXECUTABLE_PATH="$PROJECT_DIR/dist/app_desktop"

LAUNCHERS_DIR="$HOME/.local/share/applications"
mkdir -p "$LAUNCHERS_DIR"

cat > "$LAUNCHERS_DIR/yt2mp3.desktop" << EOF
[Desktop Entry]
Type=Application
Name=YouTube to MP3
Comment=Download and convert YouTube videos to MP3
Exec="$EXECUTABLE_PATH"
Icon=audio-x-generic
Terminal=false
Categories=AudioVideo;Audio;
EOF

echo "==> Desktop launcher created at: $LAUNCHERS_DIR/yt2mp3.desktop"

command -v update-desktop-database &> /dev/null && update-desktop-database "$LAUNCHERS_DIR"

echo ""
echo "=================================================="
echo " Installation complete."
echo " Look for 'YouTube to MP3' in your applications menu,"
echo " or run it directly with:"
echo "   $EXECUTABLE_PATH"
echo "=================================================="
