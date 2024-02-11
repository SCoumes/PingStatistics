#!/bin/bash

# Define variables
EXECUTABLE_NAME="Pingstats"
EXECUTABLE_FILE="Pingstats"
ICON_NAME="pingstats"
ICON_FILE="pingstats.png"
DESKTOP_FILE="${EXECUTABLE_NAME}.desktop"

USER_HOME=$(eval echo ~$USER) # Get the absolute path to the user's home directory
ICONS_DIR="$USER_HOME/.local/share/icons/hicolor/256x256"
DESKTOP_DIR="$USER_HOME/.local/share/applications"
EXECUTABLE_DIR="$USER_HOME/.local/share/pingstats"

ICON_PATH="$ICONS_DIR/${ICON_FILE}"
DESKTOP_PATH="$DESKTOP_DIR/${DESKTOP_FILE}"
EXECUTABLE_PATH="$EXECUTABLE_DIR/${EXECUTABLE_FILE}"

# Check if the executable exists in the current directory
if [ ! -f "$EXECUTABLE_NAME" ]; then
    echo "Error: $EXECUTABLE_NAME not found in the current directory."
    exit  1
fi

# Check if the icon file exists in the current directory
if [ ! -f "$ICON_FILE" ]; then
    echo "Error: $ICON_FILE not found in the current directory."
    exit  1
fi

# Ensure the directories exist
mkdir -p "$ICONS_DIR"  

# Copy the icon to the icons directory
cp "$ICON_FILE" "$ICON_PATH"

# Write the .desktop file
cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=$EXECUTABLE_NAME
Exec=$EXECUTABLE_PATH
Icon=$ICON_NAME
Terminal=false
StartupNotify=true
Categories=Utility;Application;
EOF

# Make the .desktop file executable
chmod +x "$DESKTOP_FILE"

# Move the .desktop file to the applications directory
mv "$DESKTOP_FILE" "$DESKTOP_DIR"

# Create the application directory
mkdir -p "$EXECUTABLE_DIR"

# Move the executable to the application directory
mv "$EXECUTABLE_NAME" "$EXECUTABLE_PATH"

echo "Shortcut created successfully!"
