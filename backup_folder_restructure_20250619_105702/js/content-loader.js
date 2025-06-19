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

    const poemsData = [];
    
    // Apply limit for progressive loading
    const pathsToProcess = limit ? poemFilePaths.slice(0, limit) : poemFilePaths;

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
                image: frontMatter.image || '', // Add image field
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