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

    // Helper function to get poem image path
    function getPoemImagePath(poem) {
        // Create a title-to-image mapping for all poems that have images
        const titleImageMap = {
            // Long poems from main poetry section
            'Love the Ordinary': 'love-the-ordinary.png',
            'The Real Tragedy': 'the-real-tragedy.png',
            'Back to Poetry': 'back-to-poetry.png',
            'Maybe I should Quit Poetry': 'maybe-i-should-quit-poetry.png',
            'Burden of your skin': 'burden-of-your-skin.png',
            'Beauty if not free': 'beauty-if-not-free.png',
            'Dark side of my moon': 'dark-side-of-my-moon.png',
            'First Try at an Hindi Poem': 'first-try-at-an-hindi-poem.png',
            'Mistaken Midnight Poetry': 'mistaken-midnight-poetry.png',
            'Universe Glimpses in you': 'universe-glimpses-in-you.png',
            'Run': 'run.png',
            'A Sonnet too late': 'a-sonnet-too-late.png',
            'A Void of You': 'a-void-of-you.png',
            'Haikus': 'haikus.png',
            'Escape': 'escape.png',
            'Emotional Fool': 'emotional-fool.png',
            'Ode to a true love of mine': 'ode-to-a-true-love-of-mine.png',
            'If ___ only if ___': 'if-only-if.png',
            '2 winged heart': '2-winged-heart.png',
            'Timing\'s a bitch': 'timings-a-bitch.png',
            'SECRET OLD DIARY': 'secret-old-diary.png',
            'People are Books': 'people-are-books.png',
            'Bittersweet Romance: Mocha Kisses': 'bittersweet-romance-mocha-kisses.png',
            'I Say You Say': 'i-say-you-say.png',
            'Coffee': 'coffee.png',
            'Listen to me': 'listen-to-me.png',
            'Restless Heart': 'restless-heart.png',
            'Social Sieves': 'social-sieves.png',
            'Skies and Flowers': 'skies-and-flowers.png',
            'Lost Poet': 'lost-poet.png',
            'Hmm. Bland': 'hmm-bland.png',
            'Not gonna Rhyme, but waste time.': 'not-gonna-rhyme-but-waste-time.png',
            'HEY YOU!!': 'hey-you.png',
            'Where eyes take you': 'where-eyes-take-you.png',
            'Sparkle': 'sparkle.png',
            // Short poems
            'Years of Stories': 'years-of-stories.png',
            'Kogarashi': 'kogarashi.png',
            'Why Pretend': 'why-pretend.png',
            'Cold Hallways': 'cold-hallways.png',
            'Purple Hyacinth': 'purple-hyacinth.png',
            'White Hyacinths': 'white-hyacinths.png',
            'White in a Garden of Purple': 'white-in-a-garden-of-purple.png',
            'Red Clouds, Like Bloody Hell': 'red-clouds-like-bloody-hell.png',
            'I Love Winters': 'i-love-winters.png',
            'Red Spirals Odd': 'red-spirals-odd.png',
            'Yellow Flowers on Asphalt': 'yellow-flowers-on-asphalt.png',
            'Through Tunnels of Tricks': 'through-tunnels-of-tricks.png',
            'To White Flowers of Old': 'to-white-flowers-of-old.png',
            'To Flowers\' Glamour': 'to-flowers-glamour.png',
            'Bridges You Wait Upon': 'bridges-you-wait-upon.png',
            'Magnificent Aren\'t They': 'magnificent-arent-they.png',
            'Your Rhythm and Muse': 'your-rhythm-and-muse.png',
            'A Light that Never Goes Out': 'a-light-that-never-goes-out.png',
            'Colours in Sky': 'colours-in-sky.png',
            'Plants After Rain': 'plants-after-rain.png',
            'Redness like Blood': 'redness-like-blood.png',
            'Windows of Dew': 'windows-of-dew.png',
            'Drops of Jupiter': 'drops-of-jupiter.png',
            'See Through Your Heart': 'see-through-your-heart.png',
            'Shades of Grey': 'shades-of-grey.png',
            'Moon\'s Alluring Scars': 'moons-alluring-scars.png',
            'Flowers Under Streetlight': 'flowers-under-streetlight.png',
            'A Part of the Crowd': 'a-part-of-the-crowd.png',
            'Mornings with No Clouds': 'mornings-with-no-clouds.png',
            'If You Go Deep in Thought': 'if-you-go-deep-in-thought.png',
            'Before the Break of Day': 'before-the-break-of-day.png',
            'To Flowers of Crimson Pink': 'to-flowers-of-crimson-pink.png',
            'Gayish Bubbles': 'gayish-bubbles.png',
            'What is Red': 'what-is-red.png',
            'Moon Through Sky\'s Circular Frame': 'moon-through-skys-circular-frame.png',
            'It\'s the Last Day of Earth': 'its-the-last-day-of-earth.png'
        };
        
        const imageName = titleImageMap[poem.title];
        const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website';
        return imageName ? `${basePath}/assets/images/poems/${imageName}` : `${basePath}/assets/images/placeholder.png`;
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
            console.warn('[main.js] No poems data to display or poems array is empty.');
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

    console.log("Interactive Poetry Website JS Loaded and homepage content initiated.");
});