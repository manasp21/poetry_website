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
            const imageSrc = 'assets/images/placeholder.png'; // Generic placeholder
            const imageAlt = `Placeholder for ${poem.title || 'poem'}`;

            if (currentView === 'grid') {
                poemElement.className = 'poem-card';
                poemElement.innerHTML = `
                    <a href="${poemLink}" class="poem-card-link">
                        <div class="poem-card-image-placeholder">
                           <img src="${imageSrc}" alt="${imageAlt}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';">
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
                        <img src="${imageSrc}" alt="${imageAlt}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';">
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