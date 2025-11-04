---
layout: diagram
title: "Complete System Architecture"
description: "End-to-end system architecture showing all AWS services, load balancers, microservices, and data flow from users to databases."
category: "System Architecture"
complexity: "High"
tags: ['AWS', 'Infrastructure', 'Overview', 'Fargate', 'RDS']
permalink: /diagrams/01-complete-system-architecture/
---

# Complete System Architecture

End-to-end system architecture showing all AWS services, load balancers, microservices, and data flow from users to databases.

## Diagram Details

- **Category**: System Architecture
- **Complexity**: High
- **Tags**: AWS, Infrastructure, Overview, Fargate, RDS

## View Options

<div class="diagram-viewer">
  <div class="diagram-image">
  </div>
  
  <div class="diagram-actions">
    <h3>Download Options</h3>
    <div class="download-buttons">
      <a href="/40-resources/diagrams/01-complete-system-architecture.drawio" download class="btn btn-outline">Download Source (.drawio)</a>
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
