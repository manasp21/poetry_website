#!/usr/bin/env python3
"""
Simple Sequential Renaming System
=================================
Renames poems to 1.md, 2.md, 3.md... and images to 1.png, 2.png, 3.png...
Creates mapping files to track original names.
"""

import os
import json
import shutil
import glob
import re
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create backup before renaming."""
    backup_dir = f"backup_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"📦 Creating backup: {backup_dir}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup Poetry directory
    if os.path.exists('Poetry'):
        shutil.copytree('Poetry', os.path.join(backup_dir, 'Poetry'))
        print("✅ Backed up Poetry directory")
    
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

def find_all_poems():
    """Find all poem files in the repository."""
    poem_dirs = [
        'Poetry/by_language/english/lengths/short/',
        'Poetry/by_language/english/forms/free_verse/',
        'Poetry/by_language/english/forms/sonnet/',
        'Poetry/by_language/hindi/lengths/standard/'
    ]
    
    poems = []
    for poem_dir in poem_dirs:
        if os.path.exists(poem_dir):
            for poem_file in glob.glob(os.path.join(poem_dir, "*.md")):
                poems.append(poem_file)
    
    return sorted(poems)

def find_all_images():
    """Find all image files."""
    image_dir = 'assets/images/poems/'
    if os.path.exists(image_dir):
        return sorted(glob.glob(os.path.join(image_dir, "*.png")))
    return []

def rename_poems():
    """Rename all poems to sequential numbers."""
    poems = find_all_poems()
    poem_mapping = {}
    
    print(f"\n📝 Renaming {len(poems)} poems...")
    
    # Create new Poetry directory
    new_poetry_dir = 'Poetry'
    if not os.path.exists(new_poetry_dir):
        os.makedirs(new_poetry_dir, exist_ok=True)
    
    for i, poem_file in enumerate(poems, 1):
        try:
            # Read original poem
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            frontmatter, poem_content = parse_poem_frontmatter(content)
            
            # Store mapping
            poem_mapping[str(i)] = {
                "original_file": poem_file,
                "original_name": os.path.basename(poem_file),
                "title": frontmatter.get("title", "Unknown Title"),
                "author": frontmatter.get("author", "Unknown Author"),
                "language": frontmatter.get("language", "unknown"),
                "form": frontmatter.get("form", "unknown"),
                "length": frontmatter.get("length", "unknown")
            }
            
            # Create new content without image reference
            new_frontmatter = {
                "title": frontmatter.get("title", "Unknown Title"),
                "author": frontmatter.get("author", "Unknown Author"),
                "language": frontmatter.get("language", "unknown"),
                "form": frontmatter.get("form", "unknown"),
                "length": frontmatter.get("length", "unknown"),
                "image": ""  # Empty, you'll fill manually
            }
            
            # Create new file content
            new_content = "---\n"
            for key, value in new_frontmatter.items():
                new_content += f'{key}: "{value}"\n'
            new_content += "---\n" + poem_content
            
            # Write new numbered file
            new_file = os.path.join(new_poetry_dir, f"{i}.md")
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {i}.md ← {os.path.basename(poem_file)}")
            
        except Exception as e:
            print(f"❌ Error processing {poem_file}: {e}")
    
    # Save poem mapping
    with open('poem_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(poem_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created poem_mapping.json with {len(poem_mapping)} entries")
    return poem_mapping

def rename_images():
    """Rename all images to sequential numbers."""
    images = find_all_images()
    image_mapping = {}
    
    print(f"\n🖼️ Renaming {len(images)} images...")
    
    for i, image_file in enumerate(images, 1):
        try:
            original_name = os.path.basename(image_file)
            new_name = f"{i}.png"
            new_path = os.path.join('assets/images/poems', new_name)
            
            # Rename the file
            shutil.move(image_file, new_path)
            
            # Store mapping
            image_mapping[str(i)] = original_name
            
            print(f"✅ {i}.png ← {original_name}")
            
        except Exception as e:
            print(f"❌ Error processing {image_file}: {e}")
    
    # Save image mapping
    with open('image_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(image_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created image_mapping.json with {len(image_mapping)} entries")
    return image_mapping

def update_javascript_files(poem_count):
    """Update JavaScript files with new simple paths."""
    print(f"\n📜 Updating JavaScript files...")
    
    # Generate new paths
    new_paths = [f"Poetry/{i}.md" for i in range(1, poem_count + 1)]
    
    # Update content-loader.js
    if os.path.exists('js/content-loader.js'):
        try:
            with open('js/content-loader.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new paths array
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
            
            if new_content != content:
                with open('js/content-loader.js', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Updated js/content-loader.js")
            else:
                print("⚠️  Could not find poemFilePaths array in content-loader.js")
                
        except Exception as e:
            print(f"❌ Error updating content-loader.js: {e}")
    
    # Update dynamic-poem-loader.js
    if os.path.exists('js/dynamic-poem-loader.js'):
        try:
            with open('js/dynamic-poem-loader.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new paths array
            paths_array = '[\n'
            for path in new_paths:
                paths_array += f'        "{path}",\n'
            paths_array = paths_array.rstrip(',\n') + '\n    ]'
            
            # Replace the staticPaths array
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
                print("✅ Updated js/dynamic-poem-loader.js")
            else:
                print("⚠️  Could not find staticPaths array in dynamic-poem-loader.js")
                
        except Exception as e:
            print(f"❌ Error updating dynamic-poem-loader.js: {e}")

def cleanup_old_directories():
    """Remove old poem directories after successful renaming."""
    old_dirs = [
        'Poetry/by_language'
    ]
    
    print(f"\n🧹 Cleaning up old directories...")
    
    for old_dir in old_dirs:
        if os.path.exists(old_dir):
            try:
                shutil.rmtree(old_dir)
                print(f"✅ Removed {old_dir}")
            except Exception as e:
                print(f"❌ Could not remove {old_dir}: {e}")

def create_assignment_guide():
    """Create a guide for manual image assignment."""
    guide_content = """# Manual Image Assignment Guide

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
"""
    
    with open('ASSIGNMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Created ASSIGNMENT_GUIDE.md")

def main():
    print("🔄 Simple Sequential Renaming System")
    print("=" * 50)
    print("This will rename:")
    print("- Poems to: 1.md, 2.md, 3.md...")
    print("- Images to: 1.png, 2.png, 3.png...")
    print("- Create mapping files for original names")
    print("- You'll assign images manually afterward")
    print("=" * 50)
    
    # Auto-proceed (no confirmation needed for demo)
    print("\n🚀 Proceeding with renaming...")
    
    try:
        # Step 1: Create backup
        backup_dir = create_backup()
        print(f"✅ Backup created: {backup_dir}")
        
        # Step 2: Rename poems
        poem_mapping = rename_poems()
        
        # Step 3: Rename images  
        image_mapping = rename_images()
        
        # Step 4: Update JavaScript files
        update_javascript_files(len(poem_mapping))
        
        # Step 5: Clean up old directories
        cleanup_old_directories()
        
        # Step 6: Create assignment guide
        create_assignment_guide()
        
        print(f"\n🎉 Renaming Complete!")
        print("=" * 30)
        print(f"📝 Poems: {len(poem_mapping)} files renamed to 1.md, 2.md, etc.")
        print(f"🖼️  Images: {len(image_mapping)} files renamed to 1.png, 2.png, etc.")
        print(f"📁 Mappings saved:")
        print(f"   - poem_mapping.json (original poem names)")
        print(f"   - image_mapping.json (original image names)")
        print(f"📖 Read ASSIGNMENT_GUIDE.md for manual image assignment")
        
        print(f"\n🎯 Next Steps:")
        print(f"1. 📝 Edit poem files to assign images: image: \"5.png\"")
        print(f"2. 🌐 Test website locally")
        print(f"3. 🚀 Deploy when ready")
        
        print(f"\n💡 Example Assignment:")
        print(f"   Edit Poetry/1.md and change: image: \"15.png\"")
        print(f"   The poem will display with image 15.png")
        
    except Exception as e:
        print(f"\n❌ Error during renaming: {e}")
        print(f"💡 You can restore from backup: {backup_dir}")

if __name__ == "__main__":
    main()