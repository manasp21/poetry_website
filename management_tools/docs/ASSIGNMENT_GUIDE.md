# Manual Image Assignment Guide

## How to Assign Images to Poems

After the renaming process, you'll manually assign images by editing the poem files.

### Step 1: Look at Available Images
Check `image_mapping.json` to see what images are available:
```json
{
  "1": "a-leaf-in-a-sea-of-green.png",
  "2": "a-light-that-never-goes-out.png",
  "3": "jupiter-shone-different.png",
  ...
}
```

### Step 2: Edit Poem Files
Open any poem file (e.g., `Poetry/5.md`) and update the image field:

```yaml
---
title: "Some Poem Title"
author: "Manas Pandey"
language: "en"
form: "short"
length: "short"
image: "15.png"  # Choose any numbered image
---
```

### Step 3: Match by Content
- Look at the poem title and content
- Find a suitable image from the mapping
- Add the image number to the poem's YAML

### Examples:
- Poem about leaves → Use image that was originally "a-leaf-in-a-sea-of-green.png"
- Poem about Jupiter → Use image that was originally "jupiter-shone-different.png"

### Quick Assignment:
You can also do bulk find-and-replace:
- Find poems with empty `image: ""`
- Replace with appropriate image numbers
- Use text editor's find/replace feature for faster assignment

### File Structure After Assignment:
```
Poetry/
├── 1.md (image: "5.png")
├── 2.md (image: "12.png")
├── 3.md (image: "")  # Still needs assignment
└── ...

assets/images/poems/
├── 1.png
├── 2.png
├── 3.png
└── ...
```

The website will automatically display the assigned images!
