#!/bin/bash

set -e

# Get absolute path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR"
OUTPUT_DIR="$SOURCE_DIR/dist"
TOML_FILE="$SOURCE_DIR/blender_manifest.toml"

# Get project folder name (e.g., "MyAddon")
DEFAULT_NAME="$(basename "$SOURCE_DIR")"

# Optional override from command line
CUSTOM_NAME="$1"

# Read version from TOML
VERSION=$(grep '^version' "$TOML_FILE" | cut -d '=' -f2 | tr -d ' "\r')

if [[ -z "$VERSION" ]]; then
    echo "❌ Could not read version from $TOML_FILE"
    exit 1
fi

# Final name = override or folder name
FINAL_NAME="${CUSTOM_NAME:-$DEFAULT_NAME}"
ZIP_NAME="${FINAL_NAME}-${VERSION}.zip"
ZIP_PATH="${OUTPUT_DIR}/${ZIP_NAME}"

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Exclude unwanted files (relative to zip root)
EXCLUDES=(
  "./dist/*"
  "./__pycache__/*"
  "./.git/*"
  "./.gitignore"
  "./build.sh"
  "**/__pycache__/*"
  "**/*.pyc"
)

# Zip everything in the current folder
(
  cd "$SOURCE_DIR" || exit 1
  echo "📦 Creating: $ZIP_PATH"
  zip -r "$ZIP_PATH" . -x "${EXCLUDES[@]}"
)

echo "✅ Done: $ZIP_PATH"
