// js/dynamic-poem-loader.js
// Dynamic poem discovery system that automatically finds and loads poems

// Function to discover all poem files dynamically
async function discoverAllPoems() {
    const poems = [];
    
    // Define the directory structure to scan
    const directoriesToScan = [
        'Poetry/by_language/english/lengths/short/',
        'Poetry/by_language/english/forms/free_verse/',
        'Poetry/by_language/english/forms/sonnet/',
        'Poetry/by_language/hindi/lengths/standard/'
    ];
    
    // GitHub API to get repository contents
    const repoOwner = 'manasp21';
    const repoName = 'poetry_website';
    const branch = 'main';
    
    try {
        for (const directory of directoriesToScan) {
            try {
                const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${directory}?ref=${branch}`;
                const response = await fetch(apiUrl);
                
                if (response.ok) {
                    const files = await response.json();
                    
                    // Filter for markdown files
                    const markdownFiles = files.filter(file => 
                        file.name.endsWith('.md') && file.type === 'file'
                    );
                    
                    // Add file paths to poems array
                    markdownFiles.forEach(file => {
                        poems.push({
                            path: `${directory}${file.name}`,
                            name: file.name,
                            directory: directory
                        });
                    });
                }
            } catch (error) {
                console.warn(`Could not scan directory ${directory}:`, error);
                // Continue with other directories
            }
        }
    } catch (error) {
        console.error('Error discovering poems via GitHub API:', error);
        // Fallback to static list if API fails
        return getFallbackPoemPaths();
    }
    
    return poems;
}

// Fallback function with current static paths
function getFallbackPoemPaths() {
    const staticPaths = [
        "Poetry/by_language/english/lengths/short/a-leaf-in-a-sea-of-green_a-leaf-in-a-sea-of_short_en.md",
        "Poetry/by_language/english/lengths/short/a-light-that-never-goes-out_there-is-a-light-that_short_en.md",
        "Poetry/by_language/english/lengths/short/a-part-of-the-crowd_a-part-of-the-crowd_short_en.md",
        "Poetry/by_language/english/lengths/short/before-the-break-of-day_before-the-break-of-day_short_en.md",
        "Poetry/by_language/english/lengths/short/bridges-you-wait-upon_bridges-you-wait-upon_short_en.md",
        "Poetry/by_language/english/lengths/short/cold-hallways_cold-hallways_short_en.md",
        "Poetry/by_language/english/lengths/short/colours-in-sky_colours-in-sky_short_en.md",
        "Poetry/by_language/english/lengths/short/distant-lights-i-stare_distant-lights-i-stare_short_en.md",
        "Poetry/by_language/english/lengths/short/drops-of-jupiter_i-dont-know-why-how_short_en.md",
        "Poetry/by_language/english/lengths/short/flowers-under-streetlight_flowers-under-streetlight_short_en.md",
        "Poetry/by_language/english/lengths/short/gayish-bubbles_gayish-bubbles_short_en.md",
        "Poetry/by_language/english/lengths/short/i-love-winters_i-love-winters_short_en.md",
        "Poetry/by_language/english/lengths/short/if-you-go-deep-in-thought_if-you-go-deep-in-thought_short_en.md",
        "Poetry/by_language/english/lengths/short/its-the-last-day-of-earth_its-the-last-day-of-earth_short_en.md",
        "Poetry/by_language/english/lengths/short/jupiter-shone-different_in-a-sky-filled-with_short_en.md",
        "Poetry/by_language/english/lengths/short/kogarashi_kogarashi_short_en.md",
        "Poetry/by_language/english/lengths/short/light-streaks-at-night_lights-streaks-at-night_short_en.md",
        "Poetry/by_language/english/lengths/short/lights-in-a-lecture-hall_lights-in-a-lecture-hall_short_en.md",
        "Poetry/by_language/english/lengths/short/magnificent-arent-they_magnificent-arent-they_short_en.md",
        "Poetry/by_language/english/lengths/short/moon-through-skys-circular-frame_moon-through-skys-circular-frame_short_en.md",
        "Poetry/by_language/english/lengths/short/moons-alluring-scars_why-is-the-moon-so_short_en.md",
        "Poetry/by_language/english/lengths/short/mornings-with-no-clouds_mornings-with-no-clouds_short_en.md",
        "Poetry/by_language/english/lengths/short/petals-raining_petals-raining_short_en.md",
        "Poetry/by_language/english/lengths/short/plants-after-rain_plants-after-rain_short_en.md",
        "Poetry/by_language/english/lengths/short/purple-hyacinth_purple-hyacinth_short_en.md",
        "Poetry/by_language/english/lengths/short/red-clouds-like-bloody-hell_red-clouds_short_en.md",
        "Poetry/by_language/english/lengths/short/red-spirals-odd_red-spirals-odd_short_en.md",
        "Poetry/by_language/english/lengths/short/redness-glowing-like-fate_redness-glowing-like-fate_short_en.md",
        "Poetry/by_language/english/lengths/short/redness-like-blood_redness-like-blood_short_en.en.md",
        "Poetry/by_language/english/lengths/short/see-through-your-heart_see-through-your-heart_short_en.md",
        "Poetry/by_language/english/lengths/short/shades-of-grey_shades-of-grey_short_en.md",
        "Poetry/by_language/english/lengths/short/sirius-in-the-sky_sirius-in-the-sky_short_en.md",
        "Poetry/by_language/english/lengths/short/streaks-of-light_streaks-of-light_short_en.md",
        "Poetry/by_language/english/lengths/short/through-tunnels-of-tricks_through-tunnels-of-tricks_short_en.md",
        "Poetry/by_language/english/lengths/short/to-flowers-glamour_to-flowers-glamour_short_en.md",
        "Poetry/by_language/english/lengths/short/to-flowers-of-crimson-pink_to-flowers-of-crimson-pink_short_en.md",
        "Poetry/by_language/english/lengths/short/to-white-flowers-of-old_to-white-flowers-of-old_short_en.md",
        "Poetry/by_language/english/lengths/short/what-is-red_what-is-red_short_en.md",
        "Poetry/by_language/english/lengths/short/white-canvas-empty-like-void_white-canvas_short_en.md",
        "Poetry/by_language/english/lengths/short/white-hyacinths_white-hyacinths_short_en.md",
        "Poetry/by_language/english/lengths/short/white-in-a-garden-of-purple_white-in-a-garden-of-purple_short_en.md",
        "Poetry/by_language/english/lengths/short/why-pretend_why-pretend_short_en.md",
        "Poetry/by_language/english/lengths/short/windows-of-dew_windows-of-dew_short_en.md",
        "Poetry/by_language/english/lengths/short/years-of-stories_written-in-these-lines_short_en.md",
        "Poetry/by_language/english/lengths/short/yellow-flowers-on-asphalt_yellow-flowers-on-asphalt_short_en.md",
        "Poetry/by_language/english/lengths/short/your-rhythm-and-muse_your-rhythm-and-muse_short_en.md"
    ];
    
    return staticPaths.map(path => ({
        path: path,
        name: path.split('/').pop(),
        directory: path.substring(0, path.lastIndexOf('/') + 1)
    }));
}

// Enhanced poem fetching with dynamic discovery
async function fetchAllPoemsEnhanced(limit = null) {
    let poemPaths;
    
    // Try dynamic discovery first, fallback to static if needed
    try {
        const discoveredPoems = await discoverAllPoems();
        poemPaths = discoveredPoems.map(poem => poem.path);
    } catch (error) {
        console.warn('Dynamic discovery failed, using fallback:', error);
        const fallbackPoems = getFallbackPoemPaths();
        poemPaths = fallbackPoems.map(poem => poem.path);
    }
    
    const poemsData = [];
    
    // Apply limit for progressive loading
    const pathsToProcess = limit ? poemPaths.slice(0, limit) : poemPaths;

    for (const filePath of pathsToProcess) {
        try {
            const response = await fetch(`/poetry_website/${filePath}`);
            if (!response.ok) {
                console.error(`Failed to fetch ${filePath}: ${response.status} ${response.statusText}`);
                continue;
            }
            const markdownContent = await response.text();
            const { frontMatter, poemText } = parsePoemFileContent(markdownContent);
            
            const fileName = filePath.split('/').pop().replace('.md', '');

            const poemEntry = {
                id: fileName,
                ...frontMatter,
                content: poemText,
                title: frontMatter.title || 'Untitled',
                author: frontMatter.author || 'Unknown Author',
                original_path: frontMatter.original_path || filePath,
                language: frontMatter.language || 'unknown',
                form: frontMatter.form || 'unknown',
                length: frontMatter.length || 'unknown',
                image: frontMatter.image || '',
                filePath: filePath // Store original file path for admin operations
            };
            poemsData.push(poemEntry);

        } catch (error) {
            console.error(`Catastrophic error processing ${filePath}:`, error);
        }
    }
    
    console.log(`Loaded ${poemsData.length} poems from ${pathsToProcess.length} files`);
    return poemsData;
}

// Function to get total poem count for pagination
async function getTotalPoemCount() {
    try {
        const discoveredPoems = await discoverAllPoems();
        return discoveredPoems.length;
    } catch (error) {
        console.warn('Could not get dynamic count, using fallback');
        return getFallbackPoemPaths().length;
    }
}

// Export functions for use in other scripts
window.fetchAllPoemsEnhanced = fetchAllPoemsEnhanced;
window.getTotalPoemCount = getTotalPoemCount;
window.discoverAllPoems = discoverAllPoems;