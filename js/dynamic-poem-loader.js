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
        "Poetry/1/poem.md",
        "Poetry/2/poem.md",
        "Poetry/3/poem.md",
        "Poetry/4/poem.md",
        "Poetry/5/poem.md",
        "Poetry/6/poem.md",
        "Poetry/7/poem.md",
        "Poetry/8/poem.md",
        "Poetry/9/poem.md",
        "Poetry/10/poem.md",
        "Poetry/11/poem.md",
        "Poetry/12/poem.md",
        "Poetry/13/poem.md",
        "Poetry/14/poem.md",
        "Poetry/15/poem.md",
        "Poetry/16/poem.md",
        "Poetry/17/poem.md",
        "Poetry/18/poem.md",
        "Poetry/19/poem.md",
        "Poetry/20/poem.md",
        "Poetry/21/poem.md",
        "Poetry/22/poem.md",
        "Poetry/23/poem.md",
        "Poetry/24/poem.md",
        "Poetry/25/poem.md",
        "Poetry/26/poem.md",
        "Poetry/27/poem.md",
        "Poetry/28/poem.md",
        "Poetry/29/poem.md",
        "Poetry/30/poem.md",
        "Poetry/31/poem.md",
        "Poetry/32/poem.md",
        "Poetry/33/poem.md",
        "Poetry/34/poem.md",
        "Poetry/35/poem.md",
        "Poetry/36/poem.md",
        "Poetry/37/poem.md",
        "Poetry/38/poem.md",
        "Poetry/39/poem.md",
        "Poetry/40/poem.md",
        "Poetry/41/poem.md",
        "Poetry/42/poem.md",
        "Poetry/43/poem.md",
        "Poetry/44/poem.md",
        "Poetry/45/poem.md",
        "Poetry/46/poem.md",
        "Poetry/47/poem.md",
        "Poetry/48/poem.md",
        "Poetry/49/poem.md",
        "Poetry/50/poem.md",
        "Poetry/51/poem.md",
        "Poetry/52/poem.md",
        "Poetry/53/poem.md",
        "Poetry/54/poem.md",
        "Poetry/55/poem.md",
        "Poetry/56/poem.md",
        "Poetry/57/poem.md",
        "Poetry/58/poem.md",
        "Poetry/59/poem.md",
        "Poetry/60/poem.md",
        "Poetry/61/poem.md",
        "Poetry/62/poem.md",
        "Poetry/63/poem.md",
        "Poetry/64/poem.md",
        "Poetry/65/poem.md",
        "Poetry/66/poem.md",
        "Poetry/67/poem.md",
        "Poetry/68/poem.md",
        "Poetry/69/poem.md",
        "Poetry/70/poem.md",
        "Poetry/71/poem.md",
        "Poetry/72/poem.md",
        "Poetry/73/poem.md",
        "Poetry/74/poem.md"
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