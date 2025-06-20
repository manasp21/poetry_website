// js/content-loader.js

// Function to parse YAML front matter and content from a .md file
function parsePoemFileContent(markdownContent) {
    const frontMatterRegex = /^---\s*([\s\S]*?)\s*---/;
    const match = frontMatterRegex.exec(markdownContent);

    let frontMatter = {};
    let poemText = markdownContent.trim();

    if (match) {
        const frontMatterString = match[1];
        poemText = markdownContent.substring(match[0].length).trim();
        
        // Basic YAML parsing with quoted string handling
        frontMatterString.split('\n').forEach(line => {
            const parts = line.split(':');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                let value = parts.slice(1).join(':').trim();
                
                // Remove surrounding quotes if present
                if ((value.startsWith('"') && value.endsWith('"')) || 
                    (value.startsWith("'") && value.endsWith("'"))) {
                    value = value.slice(1, -1);
                }
                
                frontMatter[key] = value;
            }
        });
    }
    return { frontMatter, poemText };
}

// Function to fetch and parse poems progressively

    // Automatic image detection for folder structure
    function getImagePathForPoem(poemPath) {
        // Convert Poetry/X/poem.md to Poetry/X/image.png
        const folderPath = poemPath.substring(0, poemPath.lastIndexOf('/'));
        return folderPath + '/image.png';
    }

// Function to fetch and parse poems progressively
async function fetchAllPoems(limit = null) {
    // Try to use enhanced dynamic loader if available, otherwise fallback to static
    if (typeof window.fetchAllPoemsEnhanced === 'function') {
        try {
            return await window.fetchAllPoemsEnhanced(limit);
        } catch (error) {
            console.warn('Enhanced loader failed, using fallback:', error);
        }
    }
    
    // Fallback to static poem list
    const poemFilePaths = [
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
        "Poetry/74/poem.md",
        "Poetry/75/poem.md"
    ];

    const poemsData = [];
    
    // Apply limit for progressive loading
    const pathsToProcess = limit ? poemFilePaths.slice(0, limit) : poemFilePaths;

    for (const filePath of pathsToProcess) {
        try {
            // Fix: Use proper base path detection like image functions
            const basePath = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? '' : '/poetry_website';
            const response = await fetch(`${basePath}/${filePath}`);
            if (!response.ok) {
                console.error(`Failed to fetch ${filePath}: ${response.status} ${response.statusText}`);
                continue;
            }
            const markdownContent = await response.text();
            const { frontMatter, poemText } = parsePoemFileContent(markdownContent);
            
            // Fix: Use folder number as ID instead of filename (all are "poem.md")
            const pathParts = filePath.split('/');
            const folderNumber = pathParts[pathParts.length - 2]; // Get "1", "2", etc. from "Poetry/1/poem.md"
            const fileName = filePath.split('/').pop().replace('.md', '');

            const poemEntry = {
                id: folderNumber,
                ...frontMatter,
                content: poemText,
                title: frontMatter.title || 'Untitled',
                author: frontMatter.author || 'Unknown Author',
                original_path: frontMatter.original_path || filePath,
                language: frontMatter.language || 'unknown',
                form: frontMatter.form || 'unknown',
                length: frontMatter.length || 'unknown',
                image: getImagePathForPoem(filePath), // Automatic image detection
            };
            poemsData.push(poemEntry);

        } catch (error) {
            console.error(`Catastrophic error processing ${filePath}:`, error);
        }
    }
    // console.log('fetchAllPoems finished. Final poemsData count:', poemsData.length);
    // if (poemsData.length < poemFilePaths.length) {
    //     console.warn(`Expected ${poemFilePaths.length} poems, but only parsed ${poemsData.length}. Check for fetch/parse errors above.`);
    // }
    // console.log('Final poemsData object:', poemsData);
    return poemsData;
}

// Expose the function if using modules, or make it global
// export { fetchAllPoems }; // For ES modules
// Or for simple script include:
window.fetchAllPoems = fetchAllPoems;
window.parsePoemFileContent = parsePoemFileContent; // also expose for potential reuse

// Added a comment to trigger a new GitHub Pages deployment. (Attempt 3)