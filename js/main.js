document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    // Theme Toggle Functionality
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = themeToggle ? themeToggle.querySelector('.sun-icon') : null;
    const moonIcon = themeToggle ? themeToggle.querySelector('.moon-icon') : null;

    const applyTheme = (theme) => {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        } else {
            body.classList.remove('dark-mode');
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        }
    };

    // Apply fade-in on page load
    body.style.opacity = '0';
    requestAnimationFrame(() => { // Ensure initial styles are applied
        body.style.transition = 'opacity 0.5s ease-in-out';
        body.style.opacity = '1';
    });

    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        } else {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            applyTheme(prefersDark ? 'dark' : 'light');
        }

        themeToggle.addEventListener('click', () => {
            const currentTheme = body.classList.contains('dark-mode') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            const newTheme = e.matches ? 'dark' : 'light';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // Update Copyright Year
    const currentYearSpan = document.getElementById('current-year');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // Helper function to generate excerpt
    function generateExcerpt(text, maxLength = 100) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        let excerpt = text.substring(0, maxLength);
        const lastSpace = excerpt.lastIndexOf(' ');
        if (lastSpace > 0 && lastSpace > maxLength - 20) {
            excerpt = excerpt.substring(0, lastSpace);
        }
        return excerpt + '...';
    }

    // Helper function to get poem image path - much simpler approach
    function getPoemImagePath(poem) {
        const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website';
        
        // Use the image field directly from poem data
        if (poem.image && poem.image.trim() !== '') {
            const imagePath = `${basePath}/assets/images/poems/${poem.image}`;
            return imagePath;
        }
        
        // Fallback to placeholder
        return `${basePath}/assets/images/placeholder.png`;
    }

    // Function to load poems and populate the homepage
    async function loadAndDisplayHomepageContent() {
        if (typeof window.fetchAllPoems !== 'function') {
            console.error('fetchAllPoems function not found. Make sure content-loader.js is loaded.');
            return;
        }

        const poems = await window.fetchAllPoems();
        const poemGrid = document.querySelector('.poem-grid');

        if (!poemGrid) {
            console.error('Poem grid container not found.');
            return;
        }

        // Add loading indicator
        poemGrid.innerHTML = '<div class="loading-message"><p>Loading poems...</p></div>';

        if (!poems || poems.length === 0) {
            poemGrid.innerHTML = '<div class="loading-message"><p>No poems found to display.</p><p>Please check back later.</p></div>'; // Fallback message
            return;
        }

        // Clear loading and add poems
        poemGrid.innerHTML = '';

        poems.forEach(poem => {
            const card = document.createElement('article');
            card.classList.add('poem-card');

            const link = document.createElement('a');
            link.classList.add('poem-card-link');
            link.href = `poem.html?id=${poem.id}`;

            const imagePlaceholder = document.createElement('div');
            imagePlaceholder.classList.add('poem-card-image-placeholder');
            const img = document.createElement('img');
            img.src = getPoemImagePath(poem);
            img.alt = `Image for ${poem.title || 'poem'}`;
            img.loading = 'lazy'; // Add lazy loading for better performance
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.3s ease-in-out';
            
            img.onload = () => {
                img.style.opacity = '1';
            };
            
            img.onerror = () => { 
                const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website';
                img.src = `${basePath}/assets/images/placeholder.png`;
                img.style.opacity = '1';
            };
            
            imagePlaceholder.appendChild(img);

            const contentDiv = document.createElement('div');
            contentDiv.classList.add('poem-card-content');

            const titleElem = document.createElement('h2');
            titleElem.classList.add('poem-card-title');
            titleElem.textContent = poem.title || 'Untitled Poem';

            const authorElem = document.createElement('p');
            authorElem.classList.add('poem-card-author');
            authorElem.textContent = poem.author || 'Unknown Author';

            const excerptElem = document.createElement('p');
            excerptElem.classList.add('poem-card-excerpt');
            excerptElem.textContent = generateExcerpt(poem.content, 120);

            contentDiv.appendChild(titleElem);
            contentDiv.appendChild(authorElem);
            contentDiv.appendChild(excerptElem);

            link.appendChild(imagePlaceholder);
            link.appendChild(contentDiv);
            card.appendChild(link);
            poemGrid.appendChild(card);
        });

        // Re-apply interactions for newly added cards
        const allPoemCards = document.querySelectorAll('.poem-card');
        allPoemCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                // card.classList.add('poem-card-hover');
            });
            card.addEventListener('mouseleave', () => {
                // card.classList.remove('poem-card-hover');
            });
        });

        // Re-apply smooth page transitions for all relevant links
        const allNavLinks = document.querySelectorAll('header nav a, .poem-card-link');
        allNavLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href && (href.startsWith('/') || href.startsWith('.') || href.includes('.html'))) {
                    if (href === '#discover') return;

                    e.preventDefault();
                    body.style.opacity = '0';
                    setTimeout(() => {
                        window.location.href = href;
                    }, 500); // Match fade-in duration
                }
            });
        });
    }

    // Load and display content
    loadAndDisplayHomepageContent().catch(error => {
        console.error("Error loading homepage content:", error);
    });

});