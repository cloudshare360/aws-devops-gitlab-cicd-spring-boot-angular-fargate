# Draw.io Integration Setup

This repository includes comprehensive draw.io diagram integration for GitHub Pages with VS Code development support.

## 🎨 VS Code Draw.io Extension

The repository is configured with the draw.io extension for VS Code for seamless diagram editing.

### Features Included:
- **Draw.io Extension**: Edit .drawio files directly in VS Code
- **Dark Theme Support**: Optimized for development workflow
- **AWS Architecture Icons**: Pre-configured with AWS symbol libraries
- **Auto-save**: Automatic diagram saving during development

### Usage:
1. Open any `.drawio` file in VS Code
2. The draw.io editor will open automatically
3. Edit diagrams with full draw.io functionality
4. Save to commit changes

## 🚀 GitHub Pages Deployment

Automated GitHub Pages deployment with draw.io diagram rendering.

### Architecture Diagrams Included:

1. **Complete System Architecture** (`01-complete-system-architecture.drawio`)
   - End-to-end AWS infrastructure overview
   - Service relationships and data flow
   - Load balancers, microservices, databases

2. **Security Architecture** (`02-security-architecture.drawio`)
   - Multi-layered security implementation
   - AWS WAF, Shield, VPC controls
   - Threat mitigation strategies

3. **CI/CD Pipeline** (`03-cicd-pipeline.drawio`)
   - GitLab CI/CD workflow (7 stages)
   - Deployment strategies and approval gates
   - Infrastructure automation

4. **Microservices Deployment** (`04-microservices-deployment.drawio`)
   - Spring Boot microservices on Fargate
   - Service communication patterns
   - Container orchestration

5. **Data Flow Architecture** (`05-data-flow-architecture.drawio`)
   - Request processing flow
   - Event-driven communication
   - Performance optimization

## 📂 File Structure

```
├── .vscode/
│   ├── extensions.json          # VS Code extensions including draw.io
│   └── settings.json           # Draw.io extension configuration
├── .github/workflows/
│   └── deploy-pages.yml        # GitHub Actions for Pages deployment
├── 40-resources/diagrams/      # Source .drawio files
│   ├── 01-complete-system-architecture.drawio
│   ├── 02-security-architecture.drawio
│   ├── 03-cicd-pipeline.drawio
│   ├── 04-microservices-deployment.drawio
│   └── 05-data-flow-architecture.drawio
├── scripts/
│   ├── convert-drawio.sh       # Bash conversion script
│   ├── convert-drawio-simple.py # Python conversion script
│   └── generate-diagram-index.py # Generate Jekyll data
├── diagrams/                   # Generated for GitHub Pages
│   ├── assets/                 # Converted images
│   │   ├── png/               # PNG format diagrams
│   │   └── svg/               # SVG format diagrams
│   └── pages/                 # Individual diagram pages
├── _layouts/
│   └── diagram.html           # Jekyll layout for diagrams
├── _data/
│   ├── diagrams.yml           # Diagram metadata
│   └── diagram_categories.yml # Category organization
├── _config.yml                # Jekyll configuration
├── Gemfile                    # Ruby dependencies
├── package.json               # Node.js dependencies
└── index.html                 # Homepage with diagram preview
```

## 🛠️ Development Workflow

### Local Development:
```bash
# Install dependencies
npm install
bundle install

# Edit diagrams in VS Code
# Files: 40-resources/diagrams/*.drawio

# Convert diagrams locally (optional)
python3 scripts/convert-drawio-simple.py
python3 scripts/generate-diagram-index.py

# Serve Jekyll site locally
bundle exec jekyll serve --livereload
```

### Deployment:
```bash
# Automatic on push to main branch
git add .
git commit -m "Update diagrams"
git push origin main

# Manual deployment
npm run deploy
```

## 🔧 GitHub Actions Workflow

The automated deployment includes:

1. **Setup Environment**
   - Node.js 18 for tooling
   - Python 3.11 for scripts
   - Ruby/Jekyll for site generation

2. **Convert Diagrams**
   - Extract .drawio file content
   - Generate PNG/SVG images
   - Create thumbnails
   - Generate metadata

3. **Build Site**
   - Process Jekyll templates
   - Generate diagram pages
   - Create navigation structure
   - Optimize assets

4. **Deploy**
   - Upload to GitHub Pages
   - Update live site
   - Generate sitemap

## 📱 GitHub Pages Features

### Diagram Viewer:
- **Responsive Design**: Works on all devices
- **Multiple Formats**: PNG, SVG, source .drawio
- **Thumbnails**: Quick preview gallery
- **Categories**: Organized by diagram type
- **Search**: Find diagrams by tags/content

### Navigation:
- **Homepage**: Overview and getting started
- **Diagram Gallery**: All diagrams with previews
- **Individual Pages**: Detailed view for each diagram
- **Download Options**: Multiple format downloads
- **Edit Instructions**: How to modify diagrams

## 🎯 Usage Examples

### View Diagrams Online:
- Visit: `https://[username].github.io/[repository]/diagrams/`
- Click any diagram for detailed view
- Download in preferred format

### Edit Diagrams:
1. Open VS Code in repository
2. Navigate to `40-resources/diagrams/`
3. Click any `.drawio` file
4. Edit in integrated draw.io editor
5. Save and commit changes

### Add New Diagrams:
1. Create new `.drawio` file in `40-resources/diagrams/`
2. Edit metadata in `scripts/generate-diagram-index.py`
3. Commit changes
4. GitHub Actions will automatically process

## 🔍 Troubleshooting

### Common Issues:

**VS Code Extension Not Working:**
- Install recommended extensions: `Ctrl+Shift+P` → "Extensions: Show Recommended Extensions"
- Reload VS Code window

**Diagram Conversion Fails:**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify file permissions: `chmod +x scripts/*.py`

**GitHub Pages Build Fails:**
- Check workflow logs in Actions tab
- Verify Jekyll syntax in `_config.yml`
- Ensure all required files are committed

### Support:
- GitHub Issues: For bugs and feature requests
- Discussions: For questions and community support
- Wiki: Additional documentation and examples

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add/edit diagrams
4. Test locally
5. Submit pull request

## 🔗 Related Documentation

- [Draw.io Documentation](https://www.diagrams.net/doc/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)