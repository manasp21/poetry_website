document.addEventListener('DOMContentLoaded', async () => {
    console.log("Archive Page JS Loaded.");

    const filterPoetSelect = document.getElementById('filter-poet');
    const filterLanguageSelect = document.getElementById('filter-language');
    const filterFormSelect = document.getElementById('filter-form');
    const filterLengthSelect = document.getElementById('filter-length');
    const sortBySelect = document.getElementById('sort-by');
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');
    const contentArea = document.getElementById('archive-content-area');

    let allPoemsData = [];
    let currentView = 'grid'; // 'grid' or 'list'

    // Helper function to generate excerpt
    function generateExcerpt(text, maxLength = 100) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        let excerpt = text.substring(0, maxLength);
        const lastSpace = excerpt.lastIndexOf(' ');
        if (lastSpace > 0 && lastSpace > maxLength - 20) { // Ensure lastSpace is meaningful
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
    
    function populateFilterOptions(poems) {
        const poets = new Set();
        const languages = new Set();
        const forms = new Set();
        const lengths = new Set();

        poems.forEach(poem => {
            if (poem.author) poets.add(poem.author);
            if (poem.language) languages.add(poem.language);
            if (poem.form) forms.add(poem.form);
            if (poem.length) lengths.add(poem.length);
        });

        const populateSelect = (selectElement, optionsSet, currentVal) => {
            if (!selectElement) return;
            // Keep the "All" option
            const firstOption = selectElement.options[0];
            selectElement.innerHTML = '';
            selectElement.appendChild(firstOption);

            Array.from(optionsSet).sort().forEach(optionValue => {
                const option = document.createElement('option');
                option.value = optionValue;
                option.textContent = optionValue.charAt(0).toUpperCase() + optionValue.slice(1).replace(/_/g, ' ');
                selectElement.appendChild(option);
            });
            if (currentVal) selectElement.value = currentVal;
        };
        
        populateSelect(filterPoetSelect, poets, filterPoetSelect.value);
        populateSelect(filterLanguageSelect, languages, filterLanguageSelect.value);
        populateSelect(filterFormSelect, forms, filterFormSelect.value);
        populateSelect(filterLengthSelect, lengths, filterLengthSelect.value);
    }


    function renderPoems(poemsToRender) {
        if (!contentArea) {
            console.error("Content area not found for rendering poems.");
            return;
        }
        contentArea.innerHTML = ''; // Clear existing content
        contentArea.className = currentView === 'grid' ? 'poem-grid' : 'poem-list';

        if (!poemsToRender || poemsToRender.length === 0) {
            contentArea.innerHTML = '<p class="no-results">No poems match your criteria.</p>';
            return;
        }

        poemsToRender.forEach(poem => {
            const poemElement = document.createElement('article');
            const poemLink = `poem.html?id=${poem.id}`;
            const imageSrc = getPoemImagePath(poem);
            const imageAlt = `Placeholder for ${poem.title || 'poem'}`;

            if (currentView === 'grid') {
                poemElement.className = 'poem-card';
                poemElement.innerHTML = `
                    <a href="${poemLink}" class="poem-card-link">
                        <div class="poem-card-image-placeholder">
                           <img src="${imageSrc}" alt="${imageAlt}" loading="lazy" style="opacity: 0; transition: opacity 0.3s ease-in-out;" onload="this.style.opacity='1';" onerror="const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website'; this.src = basePath + '/assets/images/placeholder.png'; this.style.opacity='1';">
                        </div>
                        <div class="poem-card-content">
                            <h2 class="poem-card-title">${poem.title || 'Untitled Poem'}</h2>
                            <p class="poem-card-author">${poem.author || 'Unknown Author'}</p>
                            <p class="poem-card-excerpt">${generateExcerpt(poem.content, 80)}</p>
                        </div>
                    </a>`;
            } else { // List view
                poemElement.className = 'poem-list-item';
                poemElement.innerHTML = `
                    <div class="poem-list-item-image-placeholder">
                        <img src="${imageSrc}" alt="${imageAlt}" loading="lazy" style="opacity: 0; transition: opacity 0.3s ease-in-out;" onload="this.style.opacity='1';" onerror="const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website'; this.src = basePath + '/assets/images/placeholder.png'; this.style.opacity='1';">
                    </div>
                    <div class="poem-list-item-details">
                        <h2 class="poem-list-item-title"><a href="${poemLink}">${poem.title || 'Untitled Poem'}</a></h2>
                        <p class="poem-list-item-author">${poem.author || 'Unknown Author'}</p>
                        <p class="poem-list-item-meta">
                            Language: ${poem.language || 'N/A'},
                            Form: ${poem.form || 'N/A'},
                            Length: ${poem.length || 'N/A'}
                        </p>
                    </div>`;
            }
            contentArea.appendChild(poemElement);
        });
    }

    function applyFiltersAndSort() {
        let filteredPoems = [...allPoemsData];

        const poetFilter = filterPoetSelect ? filterPoetSelect.value : '';
        const langFilter = filterLanguageSelect ? filterLanguageSelect.value : '';
        const formFilter = filterFormSelect ? filterFormSelect.value : '';
        const lengthFilter = filterLengthSelect ? filterLengthSelect.value : '';

        if (poetFilter) {
            filteredPoems = filteredPoems.filter(p => p.author === poetFilter);
        }
        if (langFilter) {
            filteredPoems = filteredPoems.filter(p => p.language === langFilter);
        }
        if (formFilter) {
            filteredPoems = filteredPoems.filter(p => p.form === formFilter);
        }
        if (lengthFilter) {
            filteredPoems = filteredPoems.filter(p => p.length === lengthFilter);
        }

        const sortValue = sortBySelect ? sortBySelect.value : 'title_asc';
        switch (sortValue) {
            case 'title_asc':
                filteredPoems.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
                break;
            case 'title_desc':
                filteredPoems.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
                break;
            case 'poet_asc':
                filteredPoems.sort((a, b) => (a.author || '').localeCompare(b.author || ''));
                break;
            case 'poet_desc':
                filteredPoems.sort((a, b) => (b.author || '').localeCompare(a.author || ''));
                break;
        }
        renderPoems(filteredPoems);
    }

    async function initializeArchive() {
        if (typeof window.fetchAllPoems !== 'function') {
            console.error('fetchAllPoems function not found. Make sure content-loader.js is loaded.');
            if(contentArea) contentArea.innerHTML = '<p class="error-message">Error loading poem data. Content loader might be missing.</p>';
            return;
        }
        try {
            allPoemsData = await window.fetchAllPoems();
            if (!Array.isArray(allPoemsData)) {
                 console.error('fetchAllPoems did not return an array:', allPoemsData);
                 allPoemsData = []; // Ensure it's an array to prevent further errors
            }
        } catch (error) {
            console.error("Failed to fetch poems:", error);
            if(contentArea) contentArea.innerHTML = '<p class="error-message">Could not load poems. Please try again later.</p>';
            allPoemsData = []; // Ensure it's an array
        }
        
        populateFilterOptions(allPoemsData);
        applyFiltersAndSort(); // Initial render with fetched data

        // Event Listeners for filters and sorters
        [filterPoetSelect, filterLanguageSelect, filterFormSelect, filterLengthSelect, sortBySelect].forEach(select => {
            if (select) select.addEventListener('change', applyFiltersAndSort);
        });

        // View Toggle Logic
        if (gridViewBtn && listViewBtn && contentArea) {
            gridViewBtn.addEventListener('click', () => {
                if (currentView !== 'grid') {
                    currentView = 'grid';
                    gridViewBtn.classList.add('active');
                    listViewBtn.classList.remove('active');
                    applyFiltersAndSort();
                }
            });

            listViewBtn.addEventListener('click', () => {
                if (currentView !== 'list') {
                    currentView = 'list';
                    listViewBtn.classList.add('active');
                    gridViewBtn.classList.remove('active');
                    applyFiltersAndSort();
                }
            });
        }
    }

    initializeArchive().catch(error => {
        console.error("Error initializing archive page:", error);
        if(contentArea) contentArea.innerHTML = '<p class="error-message">An unexpected error occurred while loading the archive.</p>';
    });
});