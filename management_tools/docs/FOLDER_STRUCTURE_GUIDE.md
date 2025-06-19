# Folder-Based Poetry Structure Guide

## New Structure Overview

Each poem now has its own folder containing both the poem file and its image:

```
Poetry/
├── 1/
│   ├── poem.md     # The poem content
│   └── image.png   # Automatically detected image
├── 2/
│   ├── poem.md
│   └── image.png
└── ...
```

## Key Benefits

✅ **Automatic Image Detection**: No need to specify image in YAML
✅ **Self-Contained**: Each poem folder has everything needed
✅ **Easy Management**: Add new poems by creating folder + files
✅ **No Manual Assignment**: Images automatically associated

## Adding New Poems

To add a new poem:

1. Create new folder: `Poetry/75/`
2. Add poem file: `Poetry/75/poem.md`
3. Add image file: `Poetry/75/image.png`
4. Done! Image automatically detected.

### Poem File Format:
```yaml
---
title: "Your Poem Title"
author: "Author Name"
language: "en"
form: "short"
length: "short"
---
Your poem content here...
```

Note: No `image:` field needed - automatically detected!

## Supported Image Formats

The system will automatically detect:
- `image.png` (preferred)
- `image.jpg`
- `image.jpeg`
- `image.webp`

## Managing Images

### Adding Image to Existing Poem:
Simply copy your image to the poem folder as `image.png`:
```bash
cp my-image.png Poetry/15/image.png
```

### Changing Image:
Replace the existing image file:
```bash
rm Poetry/15/image.png
cp new-image.png Poetry/15/image.png
```

### Multiple Images:
Currently supports one image per poem. Additional images can be added with different names but only `image.*` will be auto-detected.

## Frontend Compatibility

✅ Website looks exactly the same
✅ All existing functionality preserved
✅ No user-visible changes
✅ All poems automatically display with their images

## Technical Notes

- JavaScript automatically detects images in each poem folder
- Paths are GitHub Pages compatible
- No manual image assignment needed
- Cleaner YAML frontmatter (no image field)
- Better organized file structure

## Troubleshooting

**Poem not showing image?**
- Check that image file exists in poem folder
- Ensure image is named `image.png` (or .jpg, .jpeg, .webp)
- Verify image file is not corrupted

**Adding new poems?**
- Create folder with sequential number
- Add both poem.md and image.png
- No additional configuration needed

**Need to reorganize?**
- Poems can be renumbered by renaming folders
- Images move with their poems automatically
- No path updates needed in files

The new structure is designed to be simple, automatic, and maintainable!
