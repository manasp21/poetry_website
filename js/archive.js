document.addEventListener('DOMContentLoaded', async () => {

    // Filter and control elements
    const filterPoetSelect = document.getElementById('filter-poet');
    const filterLanguageSelect = document.getElementById('filter-language');
    const filterFormSelect = document.getElementById('filter-form');
    const filterLengthSelect = document.getElementById('filter-length');
    const sortBySelect = document.getElementById('sort-by');
    
    // View control elements
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');
    const compactViewBtn = document.getElementById('compact-view-btn');
    const contentArea = document.getElementById('archive-content-area');
    
    // Search elements
    const searchInput = document.getElementById('search-input');
    const searchClear = document.getElementById('search-clear');
    
    // Filter panel elements
    const toggleFiltersBtn = document.getElementById('toggle-filters');
    const filtersPanel = document.getElementById('filters-panel');
    const clearAllFiltersBtn = document.getElementById('clear-all-filters');
    const activeFiltersCount = document.getElementById('active-filters-count');
    
    // Stats and info elements
    const poemsCount = document.getElementById('poems-count');
    const filteredCount = document.getElementById('filtered-count');
    const showingCount = document.getElementById('showing-count');
    
    // Action buttons
    const shuffleBtn = document.getElementById('shuffle-btn');
    const selectRandomBtn = document.getElementById('select-random');

    let allPoemsData = [];
    let filteredPoemsData = [];
    let currentView = 'grid'; // 'grid', 'list', or 'compact'
    let isFiltersOpen = false;
    let searchQuery = '';

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
    
    // Search function with fuzzy matching
    function searchPoems(poems, query) {
        if (!query || query.trim() === '') return poems;
        
        const searchTerm = query.toLowerCase().trim();
        const words = searchTerm.split(/\s+/);
        
        return poems.filter(poem => {
            const searchableText = [
                poem.title || '',
                poem.author || '',
                poem.content || '',
                poem.form || '',
                poem.language || ''
            ].join(' ').toLowerCase();
            
            // Match if all words are found in the searchable text
            return words.every(word => searchableText.includes(word));
        });
    }
    
    // Update filter badge and clear button visibility
    function updateFilterIndicators() {
        const activeFilters = [
            filterPoetSelect?.value,
            filterLanguageSelect?.value,
            filterFormSelect?.value,
            filterLengthSelect?.value
        ].filter(val => val && val.trim() !== '').length;
        
        const hasSearch = searchQuery.trim() !== '';
        const totalActive = activeFilters + (hasSearch ? 1 : 0);
        
        if (activeFiltersCount) {
            activeFiltersCount.textContent = totalActive;
            activeFiltersCount.style.display = totalActive > 0 ? 'inline' : 'none';
        }
        
        if (clearAllFiltersBtn) {
            clearAllFiltersBtn.style.display = totalActive > 0 ? 'inline-block' : 'none';
        }
    }
    
    // Update stats display
    function updateStats() {
        if (poemsCount) {
            poemsCount.textContent = `${allPoemsData.length} poems total`;
        }
        
        if (showingCount) {
            const showing = filteredPoemsData.length;
            const total = allPoemsData.length;
            
            if (showing === total) {
                showingCount.textContent = `Showing all ${total} poems`;
            } else {
                showingCount.textContent = `Showing ${showing} of ${total} poems`;
            }
        }
        
        if (filteredCount) {
            const showing = filteredPoemsData.length;
            const total = allPoemsData.length;
            
            if (showing < total) {
                filteredCount.textContent = `(${showing} filtered)`;
                filteredCount.style.display = 'inline';
            } else {
                filteredCount.style.display = 'none';
            }
        }
    }
    
    // Helper function to get poem image path - updated for folder structure
    function getPoemImagePath(poem) {
        const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website';
        
        // Use the image field directly from poem data (already contains correct path)
        if (poem.image && poem.image.trim() !== '') {
            return `${basePath}/${poem.image}`;
        }
        
        // Fallback to placeholder
        return `${basePath}/assets/images/placeholder.png`;
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
                // Format the display text nicely
                let displayText = optionValue;
                if (typeof optionValue === 'string') {
                    displayText = optionValue
                        .charAt(0).toUpperCase() + 
                        optionValue.slice(1)
                        .replace(/_/g, ' ')
                        .replace(/\b\w/g, l => l.toUpperCase());
                }
                option.textContent = displayText;
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
        
        contentArea.innerHTML = '';
        
        // Set appropriate class based on view
        let containerClass = 'poem-grid';
        if (currentView === 'list') containerClass = 'poem-list';
        if (currentView === 'compact') containerClass = 'poem-compact';
        contentArea.className = containerClass;

        if (!poemsToRender || poemsToRender.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'no-results';
            noResults.innerHTML = `
                <div class="no-results-content">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="48px" height="48px">
                        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                    </svg>
                    <h3>No poems found</h3>
                    <p>Try adjusting your search terms or filters</p>
                    <button onclick="document.getElementById('clear-all-filters').click()" class="clear-filters-btn">Clear all filters</button>
                </div>
            `;
            contentArea.appendChild(noResults);
            return;
        }

        poemsToRender.forEach(poem => {
            const poemElement = document.createElement('article');
            const poemLink = `poem.html?id=${poem.id}`;
            const imageSrc = getPoemImagePath(poem);
            const imageAlt = `Image for ${poem.title || 'poem'}`;
            const title = poem.title || 'Untitled Poem';
            const author = poem.author || 'Unknown Author';
            const excerpt = generateExcerpt(poem.content, currentView === 'compact' ? 60 : 100);

            if (currentView === 'grid') {
                poemElement.className = 'poem-card';
                poemElement.innerHTML = `
                    <a href="${poemLink}" class="poem-card-link">
                        <div class="poem-card-image-placeholder">
                           <img src="${imageSrc}" alt="${imageAlt}" loading="lazy" style="opacity: 0; transition: opacity 0.3s ease-in-out;" onload="this.style.opacity='1';" onerror="const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website'; this.src = basePath + '/assets/images/placeholder.png'; this.style.opacity='1';">
                        </div>
                        <div class="poem-card-content">
                            <h2 class="poem-card-title">${title}</h2>
                            <p class="poem-card-author">${author}</p>
                            <p class="poem-card-excerpt">${excerpt}</p>
                            <div class="poem-card-meta">
                                <span class="meta-item">${poem.form || 'N/A'}</span>
                                <span class="meta-separator">•</span>
                                <span class="meta-item">${poem.length || 'N/A'}</span>
                            </div>
                        </div>
                    </a>`;
            } else if (currentView === 'list') {
                poemElement.className = 'poem-list-item';
                poemElement.innerHTML = `
                    <div class="poem-list-item-image-placeholder">
                        <img src="${imageSrc}" alt="${imageAlt}" loading="lazy" style="opacity: 0; transition: opacity 0.3s ease-in-out;" onload="this.style.opacity='1';" onerror="const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website'; this.src = basePath + '/assets/images/placeholder.png'; this.style.opacity='1';">
                    </div>
                    <div class="poem-list-item-details">
                        <h2 class="poem-list-item-title"><a href="${poemLink}">${title}</a></h2>
                        <p class="poem-list-item-author">${author}</p>
                        <p class="poem-list-item-excerpt">${excerpt}</p>
                        <div class="poem-list-item-meta">
                            <span class="meta-tag">Language: ${poem.language || 'N/A'}</span>
                            <span class="meta-tag">Form: ${poem.form || 'N/A'}</span>
                            <span class="meta-tag">Length: ${poem.length || 'N/A'}</span>
                        </div>
                    </div>`;
            } else { // Compact view
                poemElement.className = 'poem-compact-item';
                poemElement.innerHTML = `
                    <div class="poem-compact-image">
                        <img src="${imageSrc}" alt="${imageAlt}" loading="lazy" style="opacity: 0; transition: opacity 0.3s ease-in-out;" onload="this.style.opacity='1';" onerror="const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website'; this.src = basePath + '/assets/images/placeholder.png'; this.style.opacity='1';">
                    </div>
                    <div class="poem-compact-content">
                        <h3 class="poem-compact-title"><a href="${poemLink}">${title}</a></h3>
                        <p class="poem-compact-author">${author}</p>
                        <p class="poem-compact-excerpt">${excerpt}</p>
                    </div>
                    <div class="poem-compact-meta">
                        <span class="compact-form">${poem.form || 'N/A'}</span>
                    </div>`;
            }
            contentArea.appendChild(poemElement);
        });
    }

    function applyFiltersAndSort() {
        let filteredPoems = [...allPoemsData];

        // Apply search first
        if (searchQuery && searchQuery.trim() !== '') {
            filteredPoems = searchPoems(filteredPoems, searchQuery);
        }

        // Apply filters
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

        // Apply sorting
        const sortValue = sortBySelect ? sortBySelect.value : 'title_asc';
        switch (sortValue) {
            case 'title_asc':
                filteredPoems.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
                break;
            case 'title_desc':
                filteredPoems.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
                break;
            case 'author_asc':
                filteredPoems.sort((a, b) => (a.author || '').localeCompare(b.author || ''));
                break;
            case 'author_desc':
                filteredPoems.sort((a, b) => (b.author || '').localeCompare(a.author || ''));
                break;
            case 'form_asc':
                filteredPoems.sort((a, b) => (a.form || '').localeCompare(b.form || ''));
                break;
            case 'random':
                // Fisher-Yates shuffle
                for (let i = filteredPoems.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [filteredPoems[i], filteredPoems[j]] = [filteredPoems[j], filteredPoems[i]];
                }
                break;
        }
        
        filteredPoemsData = filteredPoems;
        updateFilterIndicators();
        updateStats();
        renderPoems(filteredPoems);
    }

    async function initializeArchive() {
        if (typeof window.fetchAllPoems !== 'function') {
            console.error('fetchAllPoems function not found. Make sure content-loader.js is loaded.');
            if(contentArea) contentArea.innerHTML = '<div class="error-message"><h3>Error loading poems</h3><p>Content loader might be missing.</p></div>';
            return;
        }
        
        try {
            allPoemsData = await window.fetchAllPoems();
            if (!Array.isArray(allPoemsData)) {
                 console.error('fetchAllPoems did not return an array:', allPoemsData);
                 allPoemsData = [];
            }
        } catch (error) {
            console.error("Failed to fetch poems:", error);
            if(contentArea) contentArea.innerHTML = '<div class="error-message"><h3>Could not load poems</h3><p>Please try again later.</p></div>';
            allPoemsData = [];
        }
        
        populateFilterOptions(allPoemsData);
        applyFiltersAndSort();

        // Search functionality
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                searchQuery = e.target.value;
                applyFiltersAndSort();
                
                // Show/hide clear button
                if (searchClear) {
                    searchClear.style.display = searchQuery.trim() !== '' ? 'block' : 'none';
                }
            });
        }
        
        if (searchClear) {
            searchClear.addEventListener('click', () => {
                searchQuery = '';
                if (searchInput) searchInput.value = '';
                searchClear.style.display = 'none';
                applyFiltersAndSort();
            });
        }

        // Filter panel toggle
        if (toggleFiltersBtn && filtersPanel) {
            toggleFiltersBtn.addEventListener('click', () => {
                isFiltersOpen = !isFiltersOpen;
                filtersPanel.classList.toggle('open', isFiltersOpen);
                toggleFiltersBtn.classList.toggle('active', isFiltersOpen);
            });
        }
        
        // Clear all filters
        if (clearAllFiltersBtn) {
            clearAllFiltersBtn.addEventListener('click', () => {
                searchQuery = '';
                if (searchInput) searchInput.value = '';
                if (searchClear) searchClear.style.display = 'none';
                
                [filterPoetSelect, filterLanguageSelect, filterFormSelect, filterLengthSelect].forEach(select => {
                    if (select) select.value = '';
                });
                
                applyFiltersAndSort();
            });
        }

        // Filter change listeners
        [filterPoetSelect, filterLanguageSelect, filterFormSelect, filterLengthSelect, sortBySelect].forEach(select => {
            if (select) select.addEventListener('change', applyFiltersAndSort);
        });

        // View toggle logic
        const viewButtons = [gridViewBtn, listViewBtn, compactViewBtn];
        const views = ['grid', 'list', 'compact'];
        
        viewButtons.forEach((btn, index) => {
            if (btn) {
                btn.addEventListener('click', () => {
                    const newView = views[index];
                    if (currentView !== newView) {
                        currentView = newView;
                        viewButtons.forEach(b => b && b.classList.remove('active'));
                        btn.classList.add('active');
                        applyFiltersAndSort();
                    }
                });
            }
        });
        
        // Action buttons
        if (shuffleBtn) {
            shuffleBtn.addEventListener('click', () => {
                if (sortBySelect) {
                    sortBySelect.value = 'random';
                    applyFiltersAndSort();
                }
            });
        }
        
        if (selectRandomBtn) {
            selectRandomBtn.addEventListener('click', () => {
                if (filteredPoemsData.length > 0) {
                    const randomPoem = filteredPoemsData[Math.floor(Math.random() * filteredPoemsData.length)];
                    window.location.href = `poem.html?id=${randomPoem.id}`;
                }
            });
        }
    }

    initializeArchive().catch(error => {
        console.error("Error initializing archive page:", error);
        if(contentArea) contentArea.innerHTML = '<div class="error-message"><h3>An unexpected error occurred</h3><p>Please refresh the page to try again.</p></div>';
    });
});