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
        "Poetry/1.md",
        "Poetry/2.md",
        "Poetry/3.md",
        "Poetry/4.md",
        "Poetry/5.md",
        "Poetry/6.md",
        "Poetry/7.md",
        "Poetry/8.md",
        "Poetry/9.md",
        "Poetry/10.md",
        "Poetry/11.md",
        "Poetry/12.md",
        "Poetry/13.md",
        "Poetry/14.md",
        "Poetry/15.md",
        "Poetry/16.md",
        "Poetry/17.md",
        "Poetry/18.md",
        "Poetry/19.md",
        "Poetry/20.md",
        "Poetry/21.md",
        "Poetry/22.md",
        "Poetry/23.md",
        "Poetry/24.md",
        "Poetry/25.md",
        "Poetry/26.md",
        "Poetry/27.md",
        "Poetry/28.md",
        "Poetry/29.md",
        "Poetry/30.md",
        "Poetry/31.md",
        "Poetry/32.md",
        "Poetry/33.md",
        "Poetry/34.md",
        "Poetry/35.md",
        "Poetry/36.md",
        "Poetry/37.md",
        "Poetry/38.md",
        "Poetry/39.md",
        "Poetry/40.md",
        "Poetry/41.md",
        "Poetry/42.md",
        "Poetry/43.md",
        "Poetry/44.md",
        "Poetry/45.md",
        "Poetry/46.md",
        "Poetry/47.md",
        "Poetry/48.md",
        "Poetry/49.md",
        "Poetry/50.md",
        "Poetry/51.md",
        "Poetry/52.md",
        "Poetry/53.md",
        "Poetry/54.md",
        "Poetry/55.md",
        "Poetry/56.md",
        "Poetry/57.md",
        "Poetry/58.md",
        "Poetry/59.md",
        "Poetry/60.md",
        "Poetry/61.md",
        "Poetry/62.md",
        "Poetry/63.md",
        "Poetry/64.md",
        "Poetry/65.md",
        "Poetry/66.md",
        "Poetry/67.md",
        "Poetry/68.md",
        "Poetry/69.md",
        "Poetry/70.md",
        "Poetry/71.md",
        "Poetry/72.md",
        "Poetry/73.md",
        "Poetry/74.md"
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