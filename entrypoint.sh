#!/bin/bash

# Define constants
WEIGHTS_DIR="/app/tmp/model-weights"
declare -A MODEL_WEIGHTS=(
    ["vits"]="1LyxaagK5mBVhLvnrXwj6mPK18vIqXBSl"
    # ["vitb"]="1hkfrf68r_UPe14yn8gQg0FPvHZisY_He"
    # ["vitl"]="1aqvYAJrRThv6aZLRPjPlKs-zfF6tvpof"
)

# Create model weights directory
mkdir -p "$WEIGHTS_DIR"

# Function to download weights
download_weights() {
    local model=$1
    local file_id=$2
    local weights_file="depth_anything_v2_${model}.pth"
    local weights_path="${WEIGHTS_DIR}/${weights_file}"

    if [ ! -f "$weights_path" ]; then
        echo "Downloading ${model} model weights..."
        if gdown --id "$file_id" -O "$weights_path"; then
            echo "Successfully downloaded ${weights_file}"
        else
            echo "Failed to download ${weights_file}"
            return 1
        fi
    else
        echo "${weights_file} already exists, skipping download"
    fi
}

# Download all model weights
echo "Checking and downloading model weights..."
for model in "${!MODEL_WEIGHTS[@]}"; do
    if ! download_weights "$model" "${MODEL_WEIGHTS[$model]}"; then
        echo "Error downloading $model weights"
        exit 1
    fi
done

echo "All model weights are ready"

# Start the application
echo "Starting the application..."
exec uvicorn src.backend.main:app --host 0.0.0.0 --port 8000