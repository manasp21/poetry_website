// js/dynamic-poem-loader.js - Enhanced for Folder Structure
// Dynamic poem discovery system with automatic image detection

// Function to discover all poem files dynamically from folder structure
async function discoverAllPoemsFromFolders() {
    const poems = [];
    
    // Define the folder structure to scan
    const baseDir = 'Poetry';
    
    // GitHub API to get repository contents
    const repoOwner = 'manasp21';
    const repoName = 'poetry_website';
    const branch = 'main';
    
    try {
        // Get all numbered folders in Poetry directory
        const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${baseDir}?ref=${branch}`;
        const response = await fetch(apiUrl);
        
        if (response.ok) {
            const contents = await response.json();
            
            // Filter for numbered directories
            const poemFolders = contents.filter(item => 
                item.type === 'dir' && /^\d+$/.test(item.name)
            );
            
            // For each folder, look for poem.md
            for (const folder of poemFolders) {
                const folderName = folder.name;
                const poemPath = `${baseDir}/${folderName}/poem.md`;
                
                // Check if poem.md exists in this folder
                try {
                    const poemApiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${poemPath}?ref=${branch}`;
                    const poemResponse = await fetch(poemApiUrl);
                    
                    if (poemResponse.ok) {
                        poems.push({
                            path: poemPath,
                            name: `poem_${folderName}`,
                            directory: `${baseDir}/${folderName}/`,
                            poemNumber: folderName
                        });
                    }
                } catch (error) {
                    console.warn(`Could not check poem in folder ${folderName}:`, error);
                }
            }
            
            // Sort by poem number
            poems.sort((a, b) => parseInt(a.poemNumber) - parseInt(b.poemNumber));
        }
    } catch (error) {
        console.error('Error discovering poems from folders via GitHub API:', error);
        // Fallback to static list if API fails
        return getFallbackPoemPathsForFolders();
    }
    
    return poems;
}

// Fallback function with folder-based static paths
function getFallbackPoemPathsForFolders() {
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
        name: path.split('/').pop().replace('.md', ''),
        directory: path.substring(0, path.lastIndexOf('/') + 1),
        poemNumber: path.split('/')[1]
    }));
}

// Enhanced poem fetching with dynamic discovery and automatic image detection
async function fetchAllPoemsEnhanced(limit = null) {
    let poemPaths;
    
    // Try dynamic discovery first, fallback to static if needed
    try {
        const discoveredPoems = await discoverAllPoemsFromFolders();
        poemPaths = discoveredPoems;
    } catch (error) {
        console.warn('Dynamic discovery failed, using fallback:', error);
        const fallbackPoems = getFallbackPoemPathsForFolders();
        poemPaths = fallbackPoems;
    }
    
    const poemsData = [];
    
    // Apply limit for progressive loading
    const pathsToProcess = limit ? poemPaths.slice(0, limit) : poemPaths;

    for (const poemInfo of pathsToProcess) {
        try {
            const filePath = poemInfo.path;
            
            // Fetch poem content
            const response = await fetch(`/poetry_website/${filePath}`);
            if (!response.ok) {
                console.error(`Failed to fetch ${filePath}: ${response.status} ${response.statusText}`);
                continue;
            }
            const markdownContent = await response.text();
            const { frontMatter, poemText } = parsePoemFileContent(markdownContent);
            
            const fileName = `poem_${poemInfo.poemNumber}`;

            // Automatically detect image in the same folder
            const folderPath = poemInfo.directory.replace(/\/$/, ''); // Remove trailing slash
            const imageExtensions = ['png', 'jpg', 'jpeg', 'webp'];
            let detectedImage = '';
            
            for (const ext of imageExtensions) {
                const imagePath = `${folderPath}/image.${ext}`;
                try {
                    const imageResponse = await fetch(`/poetry_website/${imagePath}`, { method: 'HEAD' });
                    if (imageResponse.ok) {
                        detectedImage = imagePath;
                        console.log(`✅ Auto-detected image: ${imagePath}`);
                        break;
                    }
                } catch (error) {
                    // Image doesn't exist, continue checking
                }
            }
            
            if (!detectedImage) {
                console.log(`❌ No image found for poem ${poemInfo.poemNumber}`);
            }

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
                image: detectedImage, // Automatically detected image
                filePath: filePath, // Store original file path for admin operations
                poemNumber: poemInfo.poemNumber,
                folderPath: folderPath
            };
            poemsData.push(poemEntry);

        } catch (error) {
            console.error(`Catastrophic error processing ${poemInfo.path}:`, error);
        }
    }
    
    console.log(`📁 Enhanced loader: ${poemsData.length} poems from ${pathsToProcess.length} folders`);
    console.log(`🖼️  Images auto-detected: ${poemsData.filter(p => p.image).length}/${poemsData.length}`);
    return poemsData;
}

// Function to get total poem count for pagination
async function getTotalPoemCountFromFolders() {
    try {
        const discoveredPoems = await discoverAllPoemsFromFolders();
        return discoveredPoems.length;
    } catch (error) {
        console.warn('Could not get dynamic count, using fallback');
        return getFallbackPoemPathsForFolders().length;
    }
}

// Export functions for use in other scripts
window.fetchAllPoemsEnhanced = fetchAllPoemsEnhanced;
window.getTotalPoemCount = getTotalPoemCountFromFolders;
window.discoverAllPoems = discoverAllPoemsFromFolders;

console.log('📁 Dynamic poem loader initialized for folder structure');
console.log('🖼️  Enhanced with automatic image detection');