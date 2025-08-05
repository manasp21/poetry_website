# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PoetryScape is a static poetry website built with vanilla HTML, CSS, and JavaScript. The site displays a collection of poetry with automatic image detection and a modern, responsive design. It's optimized for GitHub Pages deployment and features a sophisticated management system.

## Architecture

### Content Structure
- **Poetry Directory**: `Poetry/X/` where X is the poem number (1-75)
- Each poem folder contains:
  - `poem.md`: Markdown file with YAML frontmatter containing metadata and poem content
  - `image.png`: Associated image for the poem
- **YAML Frontmatter Fields**: title, author, language, form, length

### Core Web Files
- `index.html`: Homepage with featured poem cards and progressive loading
- `poem.html`: Individual poem display page with full content and metadata
- `archive.html`: Browse/filter interface for all poems
- `css/style.css`: Main stylesheet with dark/light theme support
- `js/main.js`: General site functionality, theme toggle, homepage content loading
- `js/content-loader.js`: Core content loading system that fetches and parses poem markdown files
- `js/poem-page.js`: Individual poem page functionality
- `js/archive.js`: Archive page search and filtering functionality

### Management System
Located in `management_tools/`:
- **Python CLI**: `poetry_cli.py` - Comprehensive CRUD operations for poems, metadata, and images
- **Configuration**: `config/poetry_config.json` - Settings and metadata categories
- **Documentation**: Extensive guides in `docs/` directory
- **Scripts**: Various automation and maintenance tools in `scripts/`

## Development Commands

### Static Site Development
```bash
# Serve locally (no build process required)
python -m http.server 8000
# Access at http://localhost:8000

# Alternative with Node.js
npx http-server -p 8000
```

### Poetry Management CLI
```bash
# Run the comprehensive poetry management interface
python3 poetry_cli.py

# Run CLI tests
python3 test_poetry_cli.py

# Check specific tools
python3 management_tools/scripts/poetry_manager.py
```

### Testing and Validation
```bash
# Validate poetry collection integrity
python3 management_tools/scripts/consistency_checker.py

# Check folder structure
python3 management_tools/scripts/verify_folder_structure.py

# Generate status reports
python3 management_tools/scripts/status_summary.py
```

## JavaScript Architecture

### Content Loading System
- **Primary Loader**: `fetchAllPoems()` in `content-loader.js`
- **Path Detection**: Automatic GitHub Pages vs localhost path handling
- **Progressive Loading**: Supports limiting poem count for performance
- **Image Resolution**: Automatic image path detection using folder structure
- **YAML Parsing**: Custom frontmatter parser with quoted string handling

### Path Conventions
- **GitHub Pages**: Paths prefixed with `/poetry_website/`
- **Local Development**: No path prefix
- **Image Paths**: Automatically resolved as `Poetry/X/image.png`

## Key Features

### Poetry Management
- Full CRUD operations via Python CLI
- Metadata management (forms, lengths, languages)
- Image handling with store system
- Backup and restore capabilities
- Collection validation and repair tools

### Website Features
- Dark/light theme toggle with system preference detection
- Progressive poem loading for performance
- Responsive grid layout
- Search and filtering in archive
- Lazy image loading with fallbacks

## Current Status

### Collection State
- **75 poems** in numbered folders (Poetry/1/ through Poetry/75/)
- Each poem has YAML frontmatter with complete metadata
- All poems have associated images
- Well-structured with consistent naming conventions

### Metadata Categories
- **Forms**: Free Verse, Sonnet, short
- **Lengths**: Standard, short  
- **Languages**: English (en), Hindi (hi)
- **Default Author**: Manas Pandey

## File Structure Patterns

```
Poetry/
├── 1/
│   ├── poem.md    # YAML frontmatter + poem content
│   └── image.png  # Associated artwork
├── 2/
│   ├── poem.md
│   └── image.png
└── ...

management_tools/
├── poetry_cli.py           # Main CLI interface
├── config/
│   └── poetry_config.json  # Metadata configuration
├── docs/                   # Comprehensive documentation
├── scripts/                # Automation tools
└── logs/                   # Operation logs

js/
├── main.js                 # Homepage and general functionality
├── content-loader.js       # Core poem loading system
├── poem-page.js           # Individual poem pages
└── archive.js             # Search and filtering
```

## Development Guidelines

### Adding New Poems
1. **Via CLI**: Use `python3 poetry_cli.py` for guided creation
2. **Manual**: Create `Poetry/X/` folder with `poem.md` and `image.png`
3. **JavaScript Update**: CLI automatically updates poem paths in JS files

### Modifying Poem Paths
- CLI automatically maintains `poemFilePaths` array in `content-loader.js`
- Manual updates require editing the static array if not using CLI

### Image Management
- **Store System**: Central `image_store/` for managing images before assignment
- **Formats**: PNG, JPG, JPEG, WEBP, GIF, BMP supported
- **Conversion**: Images automatically converted to PNG for consistency

### Path Handling
- All JavaScript uses dynamic path detection for GitHub Pages compatibility
- Image paths automatically resolve using folder structure
- Fallback to placeholder for missing images

## Important Notes

- **No Build Process**: Static site with no compilation required
- **GitHub Pages Ready**: Configured with proper paths and `.nojekyll` file
- **CLI Integration**: Management tools automatically update website files
- **Backup System**: Automatic backups before destructive operations
- **Validation**: Built-in consistency checking and repair tools

## CLI Usage Quick Reference

```bash
# Interactive management
python3 poetry_cli.py

# Key CLI features:
# 1. Manage Poems - CRUD operations
# 2. Manage Metadata - Forms, lengths, languages  
# 3. Manage Images - Store system and assignment
# 4. Tools & Validation - Consistency checks, backups
# 5. Statistics - Collection analytics
```

The CLI is the primary interface for content management and automatically maintains website integration.