# Quick Start Guide for GitHub Pages Development

## 🚀 Local Development Setup

### Prerequisites:
- Ruby 3.0+ (for Jekyll)
- Node.js 18+ (for tooling)
- Python 3.11+ (for scripts)

### Install Dependencies:

```bash
# Install Ruby gems
bundle install

# Install Node.js packages
npm install

# Install Python packages (if needed)
pip install pyyaml pillow requests
```

### Development Workflow:

```bash
# 1. Convert diagrams to images
python3 scripts/convert-drawio-simple.py

# 2. Generate diagram index
python3 scripts/generate-diagram-index.py

# 3. Start Jekyll development server
bundle exec jekyll serve --livereload

# Site will be available at: http://localhost:4000
```

### File Watching:
- Jekyll automatically rebuilds on file changes
- Use `--livereload` for automatic browser refresh
- Edit diagrams in VS Code with draw.io extension

## 📁 Key Directories:

- `40-resources/diagrams/` - Source .drawio files (edit here)
- `diagrams/` - Generated GitHub Pages content
- `_data/` - Jekyll data files (auto-generated)
- `_layouts/` - Jekyll templates
- `scripts/` - Build and conversion scripts

## 🔧 Common Tasks:

### Add New Diagram:
1. Create `.drawio` file in `40-resources/diagrams/`
2. Update metadata in `scripts/generate-diagram-index.py`
3. Run conversion scripts
4. Commit and push

### Edit Existing Diagram:
1. Open `.drawio` file in VS Code
2. Use integrated draw.io editor
3. Save changes
4. Run conversion scripts if needed

### Deploy to GitHub Pages:
- Automatic on push to main branch
- Manual: `npm run deploy`

## 🐛 Troubleshooting:

**Bundle install fails:**
```bash
sudo apt-get install ruby-dev build-essential
gem install bundler
```

**Jekyll serve fails:**
```bash
bundle update
bundle exec jekyll clean
```

**Permission errors:**
```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

## 📊 Viewing Diagrams:

### In VS Code:
- Click any `.drawio` file
- Edit with full draw.io functionality
- Preview panel shows live updates

### In Browser (Local):
- Visit `http://localhost:4000/diagrams/`
- Navigate through diagram gallery
- View individual diagram pages

### GitHub Pages (Live):
- Automatic deployment on push
- Visit repository GitHub Pages URL
- Professional diagram presentation