#!/bin/bash

set -e

echo "=================================="
echo " Installing GitShield"
echo "=================================="

OS="$(uname -s)"

install_linux_dependencies() {
    if command -v apt >/dev/null 2>&1; then
        sudo apt update || true
        sudo apt install -y python3 python3-pip python3-venv pipx
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3 python3-pip python3-virtualenv pipx
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm python python-pip python-virtualenv python-pipx
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y python3 python3-pip python3-virtualenv pipx
    else
        echo "Unsupported Linux package manager."
        exit 1
    fi
}

install_macos_dependencies() {
    if ! command -v brew >/dev/null 2>&1; then
        echo "Homebrew is required on macOS."
        echo "Install it from https://brew.sh"
        exit 1
    fi

    brew install python pipx
}

if [ "$OS" = "Linux" ]; then
    install_linux_dependencies
elif [ "$OS" = "Darwin" ]; then
    install_macos_dependencies
else
    echo "Unsupported OS: $OS"
    exit 1
fi

echo "Ensuring pipx path..."
python3 -m pipx ensurepath || pipx ensurepath || true

echo "Installing GitShield with pipx..."
pipx install . --force

echo ""
echo "=================================="
echo " GitShield installed successfully"
echo "=================================="
echo ""
echo "Run:"
echo "  gitshield"
echo ""
echo "If command is not found, restart your terminal or run:"
echo '  export PATH="$HOME/.local/bin:$PATH"'