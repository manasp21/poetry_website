document.addEventListener('DOMContentLoaded', async () => {
    console.log("Poem Page JS Loaded.");

    const urlParams = new URLSearchParams(window.location.search);
    const poemId = urlParams.get('id');

    const poemTitleElement = document.querySelector('.poem-title-full');
    const poemAuthorElement = document.querySelector('.poem-author-full');
    const poemContentElement = document.querySelector('.poem-content-full');
    const poemImagePlaceholder = document.querySelector('.poem-main-image-placeholder');
    const pageTitle = document.querySelector('title'); // To update browser tab title
    
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

    function displayPoemNotFound() {
        if (poemTitleElement) poemTitleElement.textContent = "Poem Not Found";
        if (poemAuthorElement) poemAuthorElement.textContent = "";
        if (poemContentElement) poemContentElement.innerHTML = "<p>The poem you are looking for could not be found. It might have been moved or the link is incorrect.</p>";
        if (pageTitle) pageTitle.textContent = "Poem Not Found - PoetryScape";
        if (poemImagePlaceholder) {
            const img = poemImagePlaceholder.querySelector('img') || document.createElement('img');
            img.src = 'assets/images/placeholder.png'; // Default placeholder
            img.alt = 'Poem not found';
            if (!poemImagePlaceholder.contains(img)) {
                poemImagePlaceholder.innerHTML = ''; // Clear previous content
                poemImagePlaceholder.appendChild(img);
            }
        }
    }

    async function loadPoem() {
        if (!poemId) {
            console.log("No poem ID found in URL.");
            displayPoemNotFound();
            return;
        }

        if (typeof window.fetchAllPoems !== 'function') {
            console.error('fetchAllPoems function not found. Make sure content-loader.js is loaded.');
            displayPoemNotFound();
            return;
        }

        try {
            const allPoems = await window.fetchAllPoems();
            if (!Array.isArray(allPoems)) {
                console.error('fetchAllPoems did not return an array:', allPoems);
                displayPoemNotFound();
                return;
            }
            const poem = allPoems.find(p => p.id === poemId);

            if (poem) {
                if (pageTitle) pageTitle.textContent = `${poem.title || 'Untitled Poem'} - PoetryScape`;
                if (poemTitleElement) poemTitleElement.textContent = poem.title || 'Untitled Poem';
                if (poemAuthorElement) poemAuthorElement.textContent = `By ${poem.author || 'Unknown Author'}`;
                
                if (poemContentElement) {
                    poemContentElement.innerHTML = ''; // Clear existing
                    // Split content by double newlines for stanzas, then by single for lines
                    const stanzasRaw = poem.content.split(/\n\s*\n/);
                    stanzasRaw.forEach(stanzaText => {
                        if (stanzaText.trim()) {
                            const stanzaElement = document.createElement('p');
                            stanzaElement.classList.add('stanza');
                            // Preserve line breaks within stanzas
                            stanzaElement.innerHTML = stanzaText.trim().split('\n').join('<br>');
                            poemContentElement.appendChild(stanzaElement);
                        }
                    });
                }

                if (poemImagePlaceholder) {
                    const img = poemImagePlaceholder.querySelector('img') || document.createElement('img');
                    img.src = getPoemImagePath(poem);
                    img.alt = `Image for ${poem.title || 'poem'}`;
                    img.loading = 'lazy';
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
                    
                    if (!poemImagePlaceholder.contains(img)) {
                        poemImagePlaceholder.innerHTML = ''; // Clear previous content
                        poemImagePlaceholder.appendChild(img);
                    }
                }
                // Re-apply stanza hover effects if needed, though CSS is preferred
                const stanzas = document.querySelectorAll('.stanza');
                stanzas.forEach(stanza => {
                    // Add any JS-based hover effects if necessary
                });

            } else {
                console.log(`Poem with ID ${poemId} not found.`);
                displayPoemNotFound();
            }
        } catch (error) {
            console.error("Error loading poem:", error);
            displayPoemNotFound();
        }
    }

    await loadPoem();

    // Favorite Button Interaction (remains mostly the same)
    const favoriteButton = document.getElementById('favorite-poem');
    if (favoriteButton) {
        favoriteButton.addEventListener('click', () => {
            favoriteButton.classList.toggle('favorited');
            if (favoriteButton.classList.contains('favorited')) {
                favoriteButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`;
                console.log(`Poem ${poemId} favorited!`);
            } else {
                favoriteButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24px" height="24px"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>`;
                console.log(`Poem ${poemId} unfavorited.`);
            }
        });
    }

    // Audio Playback Placeholder (remains the same)
    const audioButton = document.getElementById('audio-play-pause');
    if (audioButton) {
        let isPlaying = false;
        const playIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M8 5v14l11-7z"/></svg>`;
        const pauseIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;

        audioButton.addEventListener('click', () => {
            isPlaying = !isPlaying;
            if (isPlaying) {
                audioButton.innerHTML = pauseIcon;
                audioButton.setAttribute('aria-label', 'Pause audio for poem');
                console.log("Audio playing (placeholder)...");
            } else {
                audioButton.innerHTML = playIcon;
                audioButton.setAttribute('aria-label', 'Play audio for poem');
                console.log("Audio paused (placeholder)...");
            }
        });
    }

    // Social Sharing Placeholders (remains the same)
    const shareButtons = document.querySelectorAll('.share-icon');
    shareButtons.forEach(button => {
        button.addEventListener('click', () => {
            const platform = button.getAttribute('aria-label').replace('Share on ', '');
            console.log(`Sharing poem ${poemId} on ${platform} (placeholder)...`);
        });
    });
});