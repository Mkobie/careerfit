#!/bin/bash

# Define paths
DEST_DIR="abcdata/"
ARCHIVE="$DEST_DIR/company_data.tar.gz"

# Function to extract files
extract_files() {
    if [ -f "$ARCHIVE" ]; then
        echo "Extracting $ARCHIVE to $DEST_DIR..."
        mkdir -p "$DEST_DIR"

        case "$(uname -s)" in
            Linux|Darwin)
                tar -xzf "$ARCHIVE" -C "$DEST_DIR"
                ;;
            CYGWIN*|MINGW32*|MSYS*|MINGW*)
                tar -xf "$ARCHIVE" -C "$DEST_DIR"
                ;;
            *)
                echo "Unsupported OS. Please extract manually."
                exit 1
                ;;
        esac

        echo "Extraction complete."
    else
        echo "Error: Archive $ARCHIVE not found!"
        exit 1
    fi
}

# Run the function
extract_files
