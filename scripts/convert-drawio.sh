#!/bin/bash

# Script to convert Draw.io diagrams to various formats for GitHub Pages
# This script uses draw.io's command line interface via headless Chrome

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Draw.io diagram conversion...${NC}"

# Create output directories
DIAGRAM_SOURCE_DIR="40-resources/diagrams"
OUTPUT_DIR="diagrams"
ASSETS_DIR="${OUTPUT_DIR}/assets"

mkdir -p "${OUTPUT_DIR}"
mkdir -p "${ASSETS_DIR}/png"
mkdir -p "${ASSETS_DIR}/svg"
mkdir -p "${ASSETS_DIR}/pdf"

# Check if source directory exists
if [ ! -d "${DIAGRAM_SOURCE_DIR}" ]; then
    echo -e "${RED}Error: Source directory ${DIAGRAM_SOURCE_DIR} not found${NC}"
    exit 1
fi

# Function to convert draw.io file to different formats
convert_diagram() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .drawio)
    
    echo -e "${YELLOW}Converting: ${base_name}${NC}"
    
    # Convert to PNG (high quality)
    npx @mermaid-js/mermaid-cli@latest -i "$input_file" -o "${ASSETS_DIR}/png/${base_name}.png" \
        --format png --width 1200 --height 900 --backgroundColor white || {
        echo -e "${RED}Warning: PNG conversion failed for ${base_name}, using alternative method${NC}"
        
        # Alternative: Use puppeteer to convert via draw.io online
        node -e "
        const puppeteer = require('puppeteer');
        const fs = require('fs');
        
        (async () => {
          const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
          });
          
          const page = await browser.newPage();
          await page.setViewport({ width: 1200, height: 900 });
          
          // Read the draw.io file
          const drawioContent = fs.readFileSync('$input_file', 'utf8');
          const encodedContent = encodeURIComponent(drawioContent);
          
          // Load draw.io with the diagram
          await page.goto(\`https://embed.diagrams.net/?embed=1&ui=min&spin=1&modified=unsavedChanges&proto=json&data=\${encodedContent}\`);
          
          // Wait for diagram to load
          await page.waitForTimeout(3000);
          
          // Take screenshot
          await page.screenshot({
            path: '${ASSETS_DIR}/png/${base_name}.png',
            fullPage: true,
            type: 'png'
          });
          
          await browser.close();
        })();
        " || echo -e "${RED}Alternative conversion also failed for ${base_name}${NC}"
    }
    
    # Convert to SVG
    npx @mermaid-js/mermaid-cli@latest -i "$input_file" -o "${ASSETS_DIR}/svg/${base_name}.svg" \
        --format svg --backgroundColor transparent || {
        echo -e "${RED}Warning: SVG conversion failed for ${base_name}${NC}"
    }
    
    # Create thumbnail (300x200)
    if [ -f "${ASSETS_DIR}/png/${base_name}.png" ]; then
        convert "${ASSETS_DIR}/png/${base_name}.png" -resize 300x200 "${ASSETS_DIR}/png/${base_name}_thumb.png" 2>/dev/null || {
            echo -e "${YELLOW}ImageMagick not available, skipping thumbnail generation${NC}"
        }
    fi
}

# Find and convert all .drawio files
find "${DIAGRAM_SOURCE_DIR}" -name "*.drawio" -type f | while read -r file; do
    convert_diagram "$file"
done

# Create index of diagrams
echo -e "${BLUE}Creating diagram index...${NC}"
cat > "${OUTPUT_DIR}/index.md" << 'EOF'
---
layout: default
title: Architecture Diagrams
permalink: /diagrams/
---

# Architecture Diagrams

This section contains comprehensive architecture diagrams for the AWS DevOps learning project.

## Available Diagrams

{% for diagram in site.data.diagrams %}
<div class="diagram-card">
  <h3><a href="{{ diagram.url }}">{{ diagram.title }}</a></h3>
  <div class="diagram-preview">
    <a href="{{ diagram.url }}">
      <img src="{{ diagram.thumbnail }}" alt="{{ diagram.title }}" style="max-width: 300px; height: auto;">
    </a>
  </div>
  <p>{{ diagram.description }}</p>
  <div class="diagram-formats">
    <strong>Formats:</strong>
    {% if diagram.png %}<a href="{{ diagram.png }}" class="format-link">PNG</a>{% endif %}
    {% if diagram.svg %}<a href="{{ diagram.svg }}" class="format-link">SVG</a>{% endif %}
    {% if diagram.drawio %}<a href="{{ diagram.drawio }}" class="format-link">Draw.io Source</a>{% endif %}
  </div>
</div>
{% endfor %}

## How to Use These Diagrams

1. **View Online**: Click on any diagram to view the detailed version
2. **Download**: Use the format links to download diagrams in your preferred format
3. **Edit**: Download the Draw.io source files to edit and customize
4. **Print**: PDF versions are optimized for printing and presentations

## Diagram Categories

- **System Architecture**: Complete infrastructure overview
- **Security Architecture**: Security controls and protection layers
- **CI/CD Pipeline**: Development and deployment workflow
- **Microservices**: Service architecture and communication
- **Data Flow**: Request processing and event handling

<style>
.diagram-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  background: #f9f9f9;
}

.diagram-preview {
  text-align: center;
  margin: 15px 0;
}

.diagram-preview img {
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.format-link {
  display: inline-block;
  margin: 0 10px 0 0;
  padding: 4px 8px;
  background: #007cba;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
}

.format-link:hover {
  background: #005a8b;
  color: white;
}
</style>
EOF

echo -e "${GREEN}Draw.io diagram conversion completed!${NC}"
echo -e "${BLUE}Generated files in: ${OUTPUT_DIR}${NC}"
echo -e "${BLUE}Assets created in: ${ASSETS_DIR}${NC}"