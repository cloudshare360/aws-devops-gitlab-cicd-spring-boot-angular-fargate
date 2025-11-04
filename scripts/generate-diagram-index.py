#!/usr/bin/env python3
"""
Generate diagram index data for Jekyll site
This script scans the diagrams directory and creates YAML data for Jekyll
"""

import os
import json
import yaml
from pathlib import Path

# Configuration
DIAGRAM_SOURCE_DIR = "40-resources/diagrams"
OUTPUT_DIR = "diagrams"
ASSETS_DIR = f"{OUTPUT_DIR}/assets"
DATA_DIR = "_data"

# Diagram metadata
DIAGRAM_INFO = {
    "01-complete-system-architecture.drawio": {
        "title": "Complete System Architecture",
        "description": "End-to-end system architecture showing all AWS services, load balancers, microservices, and data flow from users to databases.",
        "category": "System Architecture",
        "complexity": "High",
        "tags": ["AWS", "Infrastructure", "Overview", "Fargate", "RDS"]
    },
    "02-security-architecture.drawio": {
        "title": "Security Architecture",
        "description": "Multi-layered security implementation with AWS WAF, Shield, VPC security groups, and application-level protection mechanisms.",
        "category": "Security",
        "complexity": "High", 
        "tags": ["Security", "WAF", "Shield", "VPC", "Authentication"]
    },
    "03-cicd-pipeline.drawio": {
        "title": "CI/CD Pipeline Architecture",
        "description": "Complete GitLab CI/CD pipeline showing 7 stages from code commit to production deployment with approval gates and rollback strategies.",
        "category": "DevOps",
        "complexity": "Medium",
        "tags": ["GitLab", "CI/CD", "Pipeline", "Deployment", "Automation"]
    },
    "04-microservices-deployment.drawio": {
        "title": "Microservices Deployment",
        "description": "Detailed microservices architecture on AWS Fargate showing service communication, load balancing, and container orchestration.",
        "category": "Architecture",
        "complexity": "High",
        "tags": ["Microservices", "Fargate", "Spring Boot", "Angular", "Communication"]
    },
    "05-data-flow-architecture.drawio": {
        "title": "Data Flow Architecture", 
        "description": "Request processing flow and event-driven communication patterns showing user journeys, API gateway routing, and database operations.",
        "category": "Data Flow",
        "complexity": "Medium",
        "tags": ["Data Flow", "Events", "API Gateway", "Processing", "Observability"]
    }
}

def ensure_directories():
    """Create necessary directories"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/pages", exist_ok=True)

def scan_diagrams():
    """Scan for diagram files and generate metadata"""
    diagrams = []
    
    if not os.path.exists(DIAGRAM_SOURCE_DIR):
        print(f"Warning: {DIAGRAM_SOURCE_DIR} does not exist")
        return diagrams
    
    for file_path in Path(DIAGRAM_SOURCE_DIR).glob("*.drawio"):
        filename = file_path.name
        base_name = filename.replace(".drawio", "")
        
        # Get metadata
        info = DIAGRAM_INFO.get(filename, {
            "title": base_name.replace("-", " ").title(),
            "description": f"Architecture diagram: {base_name}",
            "category": "General",
            "complexity": "Medium",
            "tags": ["Architecture"]
        })
        
        # Check for generated assets
        png_path = f"{ASSETS_DIR}/png/{base_name}.png"
        svg_path = f"{ASSETS_DIR}/svg/{base_name}.svg" 
        thumb_path = f"{ASSETS_DIR}/png/{base_name}_thumb.png"
        
        diagram_data = {
            "id": base_name,
            "title": info["title"],
            "description": info["description"],
            "category": info["category"],
            "complexity": info["complexity"],
            "tags": info["tags"],
            "source_file": f"{DIAGRAM_SOURCE_DIR}/{filename}",
            "url": f"/diagrams/{base_name}/",
            "drawio": f"/{DIAGRAM_SOURCE_DIR}/{filename}",
        }
        
        # Add asset paths if they exist
        if os.path.exists(png_path):
            diagram_data["png"] = f"/{png_path}"
        if os.path.exists(svg_path):
            diagram_data["svg"] = f"/{svg_path}"
        if os.path.exists(thumb_path):
            diagram_data["thumbnail"] = f"/{thumb_path}"
        else:
            diagram_data["thumbnail"] = diagram_data.get("png", "/assets/img/diagram-placeholder.png")
        
        diagrams.append(diagram_data)
    
    return sorted(diagrams, key=lambda x: x["id"])

def generate_individual_pages(diagrams):
    """Generate individual pages for each diagram"""
    for diagram in diagrams:
        page_content = f"""---
layout: diagram
title: "{diagram['title']}"
description: "{diagram['description']}"
category: "{diagram['category']}"
complexity: "{diagram['complexity']}"
tags: {diagram['tags']}
permalink: /diagrams/{diagram['id']}/
---

# {diagram['title']}

{diagram['description']}

## Diagram Details

- **Category**: {diagram['category']}
- **Complexity**: {diagram['complexity']}
- **Tags**: {', '.join(diagram['tags'])}

## View Options

<div class="diagram-viewer">
  <div class="diagram-image">
"""
        
        if diagram.get('png'):
            page_content += f"""    <img src="{diagram['png']}" alt="{diagram['title']}" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
"""
        
        page_content += """  </div>
  
  <div class="diagram-actions">
    <h3>Download Options</h3>
    <div class="download-buttons">
"""
        
        if diagram.get('png'):
            page_content += f"""      <a href="{diagram['png']}" download class="btn btn-primary">Download PNG</a>
"""
        if diagram.get('svg'):
            page_content += f"""      <a href="{diagram['svg']}" download class="btn btn-secondary">Download SVG</a>
"""
        if diagram.get('drawio'):
            page_content += f"""      <a href="{diagram['drawio']}" download class="btn btn-outline">Download Source (.drawio)</a>
"""
        
        page_content += """    </div>
    
    <h3>How to Edit</h3>
    <ol>
      <li>Download the .drawio source file</li>
      <li>Open with <a href="https://app.diagrams.net/" target="_blank">draw.io</a> or VS Code with draw.io extension</li>
      <li>Edit and save your changes</li>
      <li>Export to your preferred format</li>
    </ol>
  </div>
</div>

## Related Diagrams

{% assign related_diagrams = site.data.diagrams | where_exp: "item", "item.category == page.category and item.id != page.title" %}
{% for related in related_diagrams limit:3 %}
- [{{ related.title }}]({{ related.url }}) - {{ related.description }}
{% endfor %}

<style>
.diagram-viewer {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 20px 0;
}

.diagram-image {
  flex: 2;
  min-width: 300px;
}

.diagram-actions {
  flex: 1;
  min-width: 250px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.download-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 15px 0;
}

.btn {
  display: inline-block;
  padding: 10px 15px;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007cba;
  color: white;
}

.btn-primary:hover {
  background: #005a8b;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  color: white;
}

.btn-outline {
  background: transparent;
  color: #007cba;
  border: 2px solid #007cba;
}

.btn-outline:hover {
  background: #007cba;
  color: white;
}

@media (max-width: 768px) {{
  .diagram-viewer {{
    flex-direction: column;
  }}
}}
</style>
"""
        
        # Write the page file
        page_path = f"{OUTPUT_DIR}/pages/{diagram['id']}.md"
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        with open(page_path, 'w') as f:
            f.write(page_content)

def main():
    """Main function"""
    print("Generating diagram index...")
    
    ensure_directories()
    diagrams = scan_diagrams()
    
    # Write diagrams data file for Jekyll
    diagrams_yaml_path = f"{DATA_DIR}/diagrams.yml"
    with open(diagrams_yaml_path, 'w') as f:
        yaml.dump(diagrams, f, default_flow_style=False, sort_keys=False)
    
    # Generate individual diagram pages
    generate_individual_pages(diagrams)
    
    # Create categories data
    categories = {}
    for diagram in diagrams:
        category = diagram['category']
        if category not in categories:
            categories[category] = {
                'name': category,
                'diagrams': [],
                'count': 0
            }
        categories[category]['diagrams'].append(diagram['id'])
        categories[category]['count'] += 1
    
    categories_yaml_path = f"{DATA_DIR}/diagram_categories.yml"
    with open(categories_yaml_path, 'w') as f:
        yaml.dump(list(categories.values()), f, default_flow_style=False)
    
    print(f"Generated index for {len(diagrams)} diagrams")
    print(f"Created {len(categories)} categories")
    print(f"Data files written to {DATA_DIR}/")
    print(f"Individual pages written to {OUTPUT_DIR}/pages/")

if __name__ == "__main__":
    main()