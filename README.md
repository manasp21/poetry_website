# PoetryScape

A modern, minimalist poetry website showcasing a curated collection of poems with beautiful imagery and elegant typography.

## 🌟 Features

- **Modern Design**: Clean, minimalist interface with sophisticated typography
- **Dark/Light Mode**: Seamless theme switching for comfortable reading
- **Responsive Layout**: Optimized for all devices and screen sizes
- **Poetry Archive**: Browse and filter poems by author, language, form, and length
- **Individual Poem Pages**: Dedicated pages with enhanced reading experience
- **Image Integration**: Each poem paired with corresponding visual artwork
- **Fast Loading**: Optimized performance with lazy loading and efficient caching

## 🚀 Live Demo

Visit the live website: [PoetryScape](https://manasp21.github.io/poetry_website/)

## 📁 Project Structure

```
poetry_website/
├── index.html              # Homepage with featured poems
├── poem.html               # Individual poem display page
├── archive.html             # Browse/filter all poems
├── css/
│   └── style.css           # Main stylesheet with theme support
├── js/
│   ├── content-loader.js   # Poem loading and parsing system
│   ├── main.js             # Homepage functionality
│   ├── poem-page.js        # Individual poem page logic
│   └── archive.js          # Archive filtering and display
├── assets/
│   └── images/
│       ├── placeholder.png # Fallback image
│       └── poems/          # Individual poem images
└── Poetry/
    └── by_language/
        └── english/
            └── lengths/
                └── short/  # Short poem markdown files
```

## 🎨 Content Structure

### Poem Files
- Stored as Markdown files with YAML frontmatter
- Located in `Poetry/by_language/[language]/[category]/[form|length]/`
- Naming convention: `[title]_[first-line]_[length]_[language].md`

### Example Poem File
```yaml
---
title: "Years of Stories"
author: "Manas Pandey"
original_path: "Poetry/Short_Poems/poem_1.txt"
language: "en"
form: "short"
length: "short"
image: "years-of-stories.png"
---
Written in these lines,

Are years of stories,

Ages of men have passed and flew...
```

## 🛠️ Development

### Prerequisites
- A modern web browser
- Local web server (Python, Node.js, or any static server)

### Running Locally
```bash
# Clone the repository
git clone https://github.com/manasp21/poetry_website.git
cd poetry_website

# Serve with Python (recommended)
python -m http.server 8000

# Or with Node.js
npx serve .

# Open http://localhost:8000 in your browser
```

### Adding New Poems
1. Create a new markdown file in the appropriate directory
2. Include proper YAML frontmatter with metadata
3. Add the file path to `poemFilePaths` array in `js/content-loader.js`
4. (Optional) Add corresponding image to `assets/images/poems/`

## 🎯 Architecture

### Content Loading System
- **Dynamic Loading**: Poems are fetched from markdown files at runtime
- **YAML Parsing**: Custom parser extracts metadata and content
- **GitHub Pages Compatible**: Paths configured for deployment
- **Error Handling**: Graceful fallbacks for missing content

### Image System
- **Direct Reference**: Images linked via `image` field in poem frontmatter
- **Lazy Loading**: Images load progressively for better performance
- **Fallback Support**: Automatic placeholder for missing images
- **Responsive**: Proper sizing and object-fit for all devices

### Theme System
- **CSS Variables**: Dynamic color switching
- **Local Storage**: Remembers user preference
- **System Detection**: Respects OS dark mode preference
- **Smooth Transitions**: Animated theme changes

## 📱 Browser Support

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## 🔧 Configuration

### GitHub Pages Deployment
- Repository configured with `/poetry_website/` base path
- `.nojekyll` file ensures all static files are served
- Relative paths automatically adjust for deployment environment

### Path Configuration
The site automatically detects the environment:
- **Local**: Uses relative paths
- **GitHub Pages**: Prefixes with `/poetry_website/`

## 🎨 Customization

### Theme Colors
Edit CSS variables in `css/style.css`:
```css
:root {
    --accent-color-light: #00F5D4;     /* Vibrant Teal */
    --secondary-accent-color-light: #FFC857; /* Warm Amber */
    --background-color-light: #F8F8F8; /* Off-white */
    /* ... more variables */
}
```

### Typography
- Primary font: Inter (body text)
- Heading font: Playfair Display (headings)
- Alternative: Lora (poetry content)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Manas Pandey**
- Website: [themanaspandey.com](https://www.themanaspandey.com)
- GitHub: [@manasp21](https://github.com/manasp21)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/manasp21/poetry_website/issues).

## 🌟 Acknowledgments

- Design inspired by modern minimalist poetry publications
- Images sourced and curated for each poem
- Built with vanilla web technologies for maximum compatibility

---

*"Poetry is the spontaneous overflow of powerful feelings: it takes its origin from emotion recollected in tranquility."* - William Wordsworth