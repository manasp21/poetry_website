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
        
        // Basic YAML parsing (can be made more robust if needed)
        frontMatterString.split('\n').forEach(line => {
            const parts = line.split(':');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const value = parts.slice(1).join(':').trim();
                frontMatter[key] = value;
            }
        });
    }
    return { frontMatter, poemText };
}

// Function to fetch and parse all poems
async function fetchAllPoems() {
    const poemFilePaths = [
        "Poetry/by_language/english/forms/free_verse/2-winged-heart_a-heart-was-here_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/a-void-of-you_look-at-me-once_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/back-to-poetry_this-forest_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/beauty-if-not-free_i-know-a-beautiful_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/bittersweet-romance-mocha-kisses_in-moments-sweet-where_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/burden-of-your-skin_unrelatable-are-some-things_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/coffee_coffee-stains-left-on_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/emotional-fool_you-played-the-fool_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/escape_i-left-my-home_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/hey-you_hey-you_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/hmm-bland_lost-amidst-the-sea_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/i-say-you-say_i-say_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/if-only-if_if-my-heart-had_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/listen-to-me_in-the-stillness-of_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/lost-poet_have-been-since-i_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/maybe-i-should-quit-poetry_maybe-i-should-quit_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/not-gonna-rhyme-but-waste-time_what-are-we-if_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/people-are-books_people-are-books_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/restless-heart_within-the-depths-of_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/run_fast-fast_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/secret-old-diary_as-i-move-swipe_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/skies-and-flowers_the-vast-expanse-of_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/social-sieves_in-a-world-where_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/sparkle_sparkles-in-distance_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/timings-a-bitch_time-is-a-cruel_standard_en.md",
        "Poetry/by_language/english/forms/free_verse/where-eyes-take-you_where-the-eyes-take_standard_en.md",
        "Poetry/by_language/english/forms/sonnet/a-sonnet-too-late_he-loved-her-from_sonnet_en.md",
        "Poetry/by_language/english/lengths/short/years-of-stories_written-in-these-lines_short_en.md",
        "Poetry/by_language/english/lengths/short/kogarashi_kogarashi_short_en.md",
        "Poetry/by_language/english/lengths/short/why-pretend_why-pretend_short_en.md",
        "Poetry/by_language/english/lengths/short/cold-hallways_cold-hallways_short_en.md",
        "Poetry/by_language/english/lengths/short/purple-hyacinth_purple-hyacinth_short_en.md",
        "Poetry/by_language/english/lengths/short/white-hyacinths_white-hyacinths_short_en.md",
        "Poetry/by_language/english/lengths/short/white-in-a-garden-of-purple_white-in-a-garden-of-purple_short_en.md",
        "Poetry/by_language/english/lengths/short/red-clouds-like-bloody-hell_red-clouds_short_en.md",
        "Poetry/by_language/english/lengths/short/i-love-winters_i-love-winters_short_en.md",
        "Poetry/by_language/english/lengths/short/redness-glowing-like-fate_redness-glowing-like-fate_short_en.md",
        "Poetry/by_language/english/lengths/short/sirius-in-the-sky_sirius-in-the-sky_short_en.md",
        "Poetry/by_language/english/lengths/short/lights-in-a-lecture-hall_lights-in-a-lecture-hall_short_en.md",
        "Poetry/by_language/english/lengths/short/light-streaks-at-night_lights-streaks-at-night_short_en.md",
        "Poetry/by_language/english/lengths/short/streaks-of-light_streaks-of-light_short_en.md",
        "Poetry/by_language/english/lengths/short/white-canvas-empty-like-void_white-canvas_short_en.md",
        "Poetry/by_language/english/lengths/short/distant-lights-i-stare_distant-lights-i-stare_short_en.md",
        "Poetry/by_language/english/lengths/short/jupiter-shone-different_in-a-sky-filled-with_short_en.md",
        "Poetry/by_language/english/lengths/short/a-leaf-in-a-sea-of-green_a-leaf-in-a-sea-of_short_en.md",
        "Poetry/by_language/english/lengths/short/petals-raining_petals-raining_short_en.md",
        "Poetry/by_language/english/lengths/short/red-spirals-odd_red-spirals-odd_short_en.md",
        "Poetry/by_language/english/lengths/short/yellow-flowers-on-asphalt_yellow-flowers-on-asphalt_short_en.md",
        "Poetry/by_language/english/lengths/short/through-tunnels-of-tricks_through-tunnels-of-tricks_short_en.md",
        "Poetry/by_language/english/lengths/short/to-white-flowers-of-old_to-white-flowers-of-old_short_en.md",
        "Poetry/by_language/english/lengths/short/to-flowers-glamour_to-flowers-glamour_short_en.md",
        "Poetry/by_language/english/lengths/short/bridges-you-wait-upon_bridges-you-wait-upon_short_en.md",
        "Poetry/by_language/english/lengths/short/magnificent-arent-they_magnificent-arent-they_short_en.md",
        "Poetry/by_language/english/lengths/short/your-rhythm-and-muse_your-rhythm-and-muse_short_en.md",
        "Poetry/by_language/english/lengths/short/a-light-that-never-goes-out_there-is-a-light-that_short_en.md",
        "Poetry/by_language/english/lengths/short/colours-in-sky_colours-in-sky_short_en.md",
        "Poetry/by_language/english/lengths/short/plants-after-rain_plants-after-rain_short_en.md",
        "Poetry/by_language/english/lengths/short/redness-like-blood_redness-like-blood_short_en.en.md",
        "Poetry/by_language/english/lengths/short/windows-of-dew_windows-of-dew_short_en.md",
        "Poetry/by_language/english/lengths/short/drops-of-jupiter_i-dont-know-why-how_short_en.md",
        "Poetry/by_language/english/lengths/short/see-through-your-heart_see-through-your-heart_short_en.md",
        "Poetry/by_language/english/lengths/short/shades-of-grey_shades-of-grey_short_en.md",
        "Poetry/by_language/english/lengths/short/moons-alluring-scars_why-is-the-moon-so_short_en.md",
        "Poetry/by_language/english/lengths/short/flowers-under-streetlight_flowers-under-streetlight_short_en.md",
        "Poetry/by_language/english/lengths/short/a-part-of-the-crowd_a-part-of-the-crowd_short_en.md",
        "Poetry/by_language/english/lengths/short/mornings-with-no-clouds_mornings-with-no-clouds_short_en.md",
        "Poetry/by_language/english/lengths/short/if-you-go-deep-in-thought_if-you-go-deep-in-thought_short_en.md",
        "Poetry/by_language/english/lengths/short/before-the-break-of-day_before-the-break-of-day_short_en.md",
        "Poetry/by_language/english/lengths/short/to-flowers-of-crimson-pink_to-flowers-of-crimson-pink_short_en.md",
        "Poetry/by_language/english/lengths/short/gayish-bubbles_gayish-bubbles_short_en.md",
        "Poetry/by_language/english/lengths/short/what-is-red_what-is-red_short_en.md",
        "Poetry/by_language/english/lengths/short/moon-through-skys-circular-frame_moon-through-skys-circular-frame_short_en.md",
        "Poetry/by_language/english/lengths/short/its-the-last-day-of-earth_its-the-last-day-of-earth_short_en.md",
        "Poetry/by_language/hindi/lengths/standard/hindi-poem_kitni-barishen-aa-gain_standard_hi.md"
    ];

    const poemsData = [];

    for (const filePath of poemFilePaths) {
        try {
            const response = await fetch(filePath);
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