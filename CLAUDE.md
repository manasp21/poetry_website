# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static poetry website called "PoetryScape" that displays poetry collections with a modern, minimalist design. The site is built with vanilla HTML, CSS, and JavaScript, and is designed to be deployed on GitHub Pages.

## Architecture

### Content Structure
- Poetry files are stored in markdown format under `Poetry/by_language/[language]/[category]/[form|length]/`
- Each poem file follows the naming convention: `[title]_[first-line]_[length]_[language].md`
- Poems contain YAML front matter with metadata (title, author, language, form, length, etc.)

### Core Files
- `index.html` - Homepage with featured poem cards
- `poem.html` - Individual poem display page
- `archive.html` - Browse/filter all poems
- `js/content-loader.js` - Main content loading system that fetches and parses poem markdown files
- `js/main.js` - General site functionality
- `js/poem-page.js` - Poem-specific page functionality
- `js/archive.js` - Archive page functionality
- `css/style.css` - Main stylesheet

### JavaScript Architecture
The site uses a custom content loading system:
- `fetchAllPoems()` function loads all poems from predefined file paths
- `parsePoemFileContent()` parses YAML front matter and poem content
- Poems are fetched via relative paths prefixed with `/poetry_website/` for GitHub Pages deployment

## Development Commands

This is a static site with no build process. To develop:
1. Serve the files using a local web server (e.g., `python -m http.server 8000`)
2. Access via `http://localhost:8000`

## File Path Conventions

When modifying poem paths in `content-loader.js`, ensure paths start with `/poetry_website/` for GitHub Pages compatibility.

## Design Philosophy

The site follows "ultra-modern, minimalist sophistication" principles as outlined in `design_document.md`. Key design elements include:
- Clean typography with generous whitespace
- Subtle color palettes with accent colors
- Responsive grid layouts
- Dark/light theme toggle functionality
- Focus on poetry content presentation

## Important Notes

- All poem files must be manually added to the `poemFilePaths` array in `content-loader.js`
- The site is configured for GitHub Pages deployment with `/poetry_website/` path prefix and includes `.nojekyll` file to ensure all files are served
- Placeholder images are referenced but may need path corrections
- The project includes comprehensive design documentation in `design_document.md` and enhancement plans in `project_enhancement_plan.md`