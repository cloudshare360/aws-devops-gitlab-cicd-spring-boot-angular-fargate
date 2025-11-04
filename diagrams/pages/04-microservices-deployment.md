---
layout: diagram
title: "Microservices Deployment"
description: "Detailed microservices architecture on AWS Fargate showing service communication, load balancing, and container orchestration."
category: "Architecture"
complexity: "High"
tags: ['Microservices', 'Fargate', 'Spring Boot', 'Angular', 'Communication']
permalink: /diagrams/04-microservices-deployment/
---

# Microservices Deployment

Detailed microservices architecture on AWS Fargate showing service communication, load balancing, and container orchestration.

## Diagram Details

- **Category**: Architecture
- **Complexity**: High
- **Tags**: Microservices, Fargate, Spring Boot, Angular, Communication

## View Options

<div class="diagram-viewer">
  <div class="diagram-image">
    <img src="/diagrams/assets/png/04-microservices-deployment.png" alt="Microservices Deployment" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
  </div>
  
  <div class="diagram-actions">
    <h3>Download Options</h3>
    <div class="download-buttons">
      <a href="/diagrams/assets/png/04-microservices-deployment.png" download class="btn btn-primary">Download PNG</a>
      <a href="/40-resources/diagrams/04-microservices-deployment.drawio" download class="btn btn-outline">Download Source (.drawio)</a>
    </div>
    
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
