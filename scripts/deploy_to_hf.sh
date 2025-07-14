#!/bin/bash

HF_TOKEN="${HF_TOKEN:?Please set HF_TOKEN environment variable}"
SPACE_NAME=${1:-"tabayyun-api"}
USERNAME=${2:-"ahmed-salim"}

# create a space
huggingface-cli repo create "$USERNAME/$SPACE_NAME" --repo-type space --space_sdk gradio --exist-ok

TEMP_DIR=$(mktemp -d)
cp gradio_app.py utils.py "$TEMP_DIR/"

cat > "$TEMP_DIR/requirements.txt" << 'EOF'
gradio>=4.44.0
requests>=2.31.0
python-dotenv>=1.0.0
EOF

cat > "$TEMP_DIR/README.md" << 'EOF'
---
title: Tabayyun API
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Tabayyun API

Check website information using Tabayyun API. Get risk assessment, organization details, and sector information in English and Arabic.

## Usage

1. Use custom API key or leave unchecked for environment variable
2. Enter website URL
3. Click "Check"

## API Key

Set `API_KEY` in Space settings or use the toggle in the app
EOF

cat > "$TEMP_DIR/app.py" << 'EOF'
import os
import gradio as gr
from gradio_app import demo

if __name__ == "__main__":
    demo.launch()
EOF

cd "$TEMP_DIR"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin "https://oauth2:$HF_TOKEN@huggingface.co/spaces/$USERNAME/$SPACE_NAME"
git push -u origin main --force

cd -
rm -rf "$TEMP_DIR" 