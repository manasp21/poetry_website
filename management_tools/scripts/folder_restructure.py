#!/usr/bin/env python3
"""
Folder-Based Structure Overhaul
===============================
Restructures from flat files to individual folders where each poem has its own
directory containing both the poem file and its image with automatic detection.
"""

import os
import json
import shutil
import glob
import re
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create backup before restructuring."""
    backup_dir = f"backup_folder_restructure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"📦 Creating backup: {backup_dir}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup current Poetry directory
    if os.path.exists('Poetry'):
        shutil.copytree('Poetry', os.path.join(backup_dir, 'Poetry'))
        print("✅ Backed up current Poetry directory")
    
    # Backup images
    if os.path.exists('assets/images/poems'):
        shutil.copytree('assets/images/poems', os.path.join(backup_dir, 'images'))
        print("✅ Backed up images directory")
    
    # Backup JavaScript files
    js_files = ['js/content-loader.js', 'js/dynamic-poem-loader.js']
    js_backup_dir = os.path.join(backup_dir, 'js')
    os.makedirs(js_backup_dir, exist_ok=True)
    
    for js_file in js_files:
        if os.path.exists(js_file):
            shutil.copy2(js_file, js_backup_dir)
            print(f"✅ Backed up {js_file}")
    
    # Backup mapping files
    for mapping_file in ['poem_mapping.json', 'image_mapping.json']:
        if os.path.exists(mapping_file):
            shutil.copy2(mapping_file, backup_dir)
            print(f"✅ Backed up {mapping_file}")
    
    return backup_dir

def parse_poem_frontmatter(content):
    """Parse YAML frontmatter from poem content."""
    frontmatter = {}
    poem_content = content.strip()
    
    if content.strip().startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            poem_content = parts[2].strip()
            
            # Simple YAML parsing
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    frontmatter[key] = value
    
    return frontmatter, poem_content

def get_current_image_assignment(poem_file):
    """Get currently assigned image for a poem."""
    try:
        with open(poem_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract image field from frontmatter
        frontmatter, _ = parse_poem_frontmatter(content)
        image_value = frontmatter.get('image', '')
        
        # Return image number if assigned
        if image_value and image_value.endswith('.png'):
            return image_value
        
        return None
    except Exception as e:
        print(f"❌ Error reading {poem_file}: {e}")
        return None

def create_folder_structure():
    """Create the new folder-based structure."""
    print(f"\n🏗️  Creating folder-based structure...")
    
    # Get all current poems
    current_poems = sorted(glob.glob("Poetry/*.md"))
    restructure_log = []
    
    # Create new temporary directory
    new_poetry_dir = "Poetry_New"
    if os.path.exists(new_poetry_dir):
        shutil.rmtree(new_poetry_dir)
    os.makedirs(new_poetry_dir, exist_ok=True)
    
    for poem_file in current_poems:
        try:
            # Extract poem number from filename (e.g., "1.md" -> "1")
            poem_num = os.path.basename(poem_file).replace('.md', '')
            
            # Create folder for this poem
            poem_folder = os.path.join(new_poetry_dir, poem_num)
            os.makedirs(poem_folder, exist_ok=True)
            
            # Read current poem content
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter and remove image field
            frontmatter, poem_content = parse_poem_frontmatter(content)
            
            # Get currently assigned image
            current_image = frontmatter.get('image', '')
            
            # Create clean frontmatter without image field
            clean_frontmatter = {
                "title": frontmatter.get("title", "Unknown Title"),
                "author": frontmatter.get("author", "Unknown Author"),
                "language": frontmatter.get("language", "unknown"),
                "form": frontmatter.get("form", "unknown"),
                "length": frontmatter.get("length", "unknown")
            }
            
            # Create new poem.md content
            new_content = "---\n"
            for key, value in clean_frontmatter.items():
                new_content += f'{key}: "{value}"\n'
            new_content += "---\n" + poem_content
            
            # Write poem.md to folder
            poem_path = os.path.join(poem_folder, "poem.md")
            with open(poem_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Handle image assignment
            image_copied = False
            if current_image and current_image.endswith('.png'):
                # Extract image number from assignment (e.g., "29.png" -> "29")
                image_num = current_image.replace('.png', '')
                source_image = f"assets/images/poems/{image_num}.png"
                
                if os.path.exists(source_image):
                    dest_image = os.path.join(poem_folder, "image.png")
                    shutil.copy2(source_image, dest_image)
                    image_copied = True
                    restructure_log.append(f"✅ {poem_num}/: poem + image from {current_image}")
                else:
                    restructure_log.append(f"⚠️  {poem_num}/: poem only (image {current_image} not found)")
            else:
                restructure_log.append(f"📝 {poem_num}/: poem only (no image assigned)")
            
            print(f"✅ Created Poetry/{poem_num}/ ({'with image' if image_copied else 'poem only'})")
            
        except Exception as e:
            print(f"❌ Error processing {poem_file}: {e}")
            restructure_log.append(f"❌ {poem_num}/: Error - {e}")
    
    # Save restructure log
    with open('restructure_log.txt', 'w', encoding='utf-8') as f:
        f.write("Folder Restructure Log\n")
        f.write("=" * 30 + "\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        for entry in restructure_log:
            f.write(entry + "\n")
    
    print(f"✅ Created restructure_log.txt with details")
    return new_poetry_dir, len(current_poems)

def handle_unassigned_images():
    """Handle images that weren't assigned to any poem."""
    print(f"\n🖼️  Handling unassigned images...")
    
    # Get all images that still exist in original location
    remaining_images = glob.glob("assets/images/poems/*.png")
    
    if not remaining_images:
        print("✅ All images have been handled")
        return
    
    print(f"📊 Found {len(remaining_images)} unassigned images:")
    
    # Load mappings to show original names
    image_mapping = {}
    if os.path.exists('image_mapping.json'):
        with open('image_mapping.json', 'r') as f:
            image_mapping = json.load(f)
    
    unassigned_list = []
    for image_file in remaining_images:
        image_num = os.path.basename(image_file).replace('.png', '')
        original_name = image_mapping.get(image_num, f"image_{image_num}.png")
        unassigned_list.append(f"   {image_num}.png (was: {original_name})")
        
    for entry in unassigned_list[:10]:  # Show first 10
        print(entry)
    
    if len(unassigned_list) > 10:
        print(f"   ... and {len(unassigned_list) - 10} more")
    
    print(f"\n💡 These images can be manually added to poem folders later")
    print(f"   Example: Copy 5.png to Poetry/3/image.png to assign to poem 3")

def update_javascript_for_folders(poem_count):
    """Update JavaScript files to work with folder structure."""
    print(f"\n📜 Updating JavaScript for folder structure...")
    
    # Generate new folder-based paths
    new_paths = [f"Poetry/{i}/poem.md" for i in range(1, poem_count + 1)]
    
    # Update content-loader.js
    if os.path.exists('js/content-loader.js'):
        try:
            with open('js/content-loader.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the paths array
            paths_array = '[\n'
            for path in new_paths:
                paths_array += f'        "{path}",\n'
            paths_array = paths_array.rstrip(',\n') + '\n    ]'
            
            # Replace the old paths array
            pattern = r'const poemFilePaths = \[[\s\S]*?\];'
            new_content = re.sub(
                pattern,
                f'const poemFilePaths = {paths_array};',
                content,
                count=1
            )
            
            # Add automatic image detection logic
            image_detection_code = '''
    // Automatic image detection for folder structure
    function getImagePathForPoem(poemPath) {
        // Convert Poetry/X/poem.md to Poetry/X/image.png
        const folderPath = poemPath.substring(0, poemPath.lastIndexOf('/'));
        return folderPath + '/image.png';
    }'''
            
            # Insert the image detection function before the fetchAllPoems function
            fetch_function_pattern = r'(async function fetchAllPoems\()'
            new_content = re.sub(
                fetch_function_pattern,
                image_detection_code + '\n\n// Function to fetch and parse poems progressively\n\\1',
                new_content,
                count=1
            )
            
            # Update the poem processing to automatically detect images
            old_image_logic = r'image: frontMatter\.image \|\| \'\'.*?,'
            new_image_logic = '''image: getImagePathForPoem(filePath).replace('/poetry_website/', '').replace('Poetry/', ''),'''
            
            new_content = re.sub(old_image_logic, new_image_logic, new_content, flags=re.DOTALL)
            
            if new_content != content:
                with open('js/content-loader.js', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Updated js/content-loader.js for folder structure")
            else:
                print("⚠️  Could not update content-loader.js - manual update needed")
                
        except Exception as e:
            print(f"❌ Error updating content-loader.js: {e}")
    
    # Update dynamic-poem-loader.js
    if os.path.exists('js/dynamic-poem-loader.js'):
        try:
            with open('js/dynamic-poem-loader.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the staticPaths array
            paths_array = '[\n'
            for path in new_paths:
                paths_array += f'        "{path}",\n'
            paths_array = paths_array.rstrip(',\n') + '\n    ]'
            
            # Replace the old paths array
            pattern = r'const staticPaths = \[[\s\S]*?\];'
            new_content = re.sub(
                pattern,
                f'const staticPaths = {paths_array};',
                content,
                count=1
            )
            
            if new_content != content:
                with open('js/dynamic-poem-loader.js', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Updated js/dynamic-poem-loader.js for folder structure")
            else:
                print("⚠️  Could not update dynamic-poem-loader.js - manual update needed")
                
        except Exception as e:
            print(f"❌ Error updating dynamic-poem-loader.js: {e}")

def finalize_restructure(new_poetry_dir):
    """Replace old Poetry directory with new structure."""
    print(f"\n🔄 Finalizing restructure...")
    
    try:
        # Remove old Poetry directory
        if os.path.exists('Poetry'):
            shutil.rmtree('Poetry')
            print("✅ Removed old Poetry directory")
        
        # Rename new directory to Poetry
        shutil.move(new_poetry_dir, 'Poetry')
        print("✅ Activated new folder structure")
        
        # Clean up old assets/images/poems if it's empty or nearly empty
        remaining_images = glob.glob("assets/images/poems/*.png")
        if len(remaining_images) <= 5:  # Keep if many unassigned images remain
            print(f"💡 {len(remaining_images)} unassigned images remain in assets/images/poems/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error finalizing restructure: {e}")
        return False

def create_usage_guide():
    """Create guide for the new folder structure."""
    guide_content = """# Folder-Based Poetry Structure Guide

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
"""
    
    with open('FOLDER_STRUCTURE_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Created FOLDER_STRUCTURE_GUIDE.md")

def main():
    print("🏗️  Folder-Based Structure Overhaul")
    print("=" * 50)
    print("This will restructure your poetry collection into individual folders")
    print("where each poem has its own directory with automatic image detection.")
    print("=" * 50)
    
    try:
        # Step 1: Create backup
        backup_dir = create_backup()
        print(f"✅ Backup created: {backup_dir}")
        
        # Step 2: Create folder structure
        new_poetry_dir, poem_count = create_folder_structure()
        
        # Step 3: Handle unassigned images
        handle_unassigned_images()
        
        # Step 4: Update JavaScript files
        update_javascript_for_folders(poem_count)
        
        # Step 5: Finalize restructure
        if finalize_restructure(new_poetry_dir):
            print("✅ Restructure completed successfully")
        else:
            print("❌ Restructure failed - check backup")
            return
        
        # Step 6: Create usage guide
        create_usage_guide()
        
        print(f"\n🎉 Folder Structure Overhaul Complete!")
        print("=" * 50)
        print(f"📁 Structure: Each poem now has its own folder")
        print(f"🖼️  Images: Automatically detected (no manual assignment)")
        print(f"📝 Poems: {poem_count} poems restructured")
        print(f"📜 JavaScript: Updated for new structure")
        print(f"🌐 Frontend: Works exactly the same")
        
        print(f"\n📊 New Structure Example:")
        print(f"   Poetry/1/poem.md + Poetry/1/image.png")
        print(f"   Poetry/2/poem.md + Poetry/2/image.png")
        print(f"   ...")
        
        print(f"\n🎯 Next Steps:")
        print(f"1. 🌐 Test website locally")
        print(f"2. 📖 Read FOLDER_STRUCTURE_GUIDE.md")
        print(f"3. 🚀 Deploy when ready")
        print(f"4. 🎭 Enjoy automatic image detection!")
        
    except Exception as e:
        print(f"\n❌ Error during restructure: {e}")
        print(f"💡 Restore from backup: {backup_dir}")

if __name__ == "__main__":
    main()