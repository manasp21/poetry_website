#!/usr/bin/env python3
"""
Poetry Collection Status Summary
================================
Quick overview of your poetry collection status and next steps.
"""

import os
import json
import glob
from pathlib import Path

def main():
    print("🎭 PoetryScape Collection Status Summary")
    print("=" * 50)
    
    # Check if registry exists
    registry_exists = os.path.exists('poem_registry.json')
    
    if registry_exists:
        with open('poem_registry.json', 'r') as f:
            registry = json.load(f)
        poems_count = len(registry.get('poems', {}))
        images_count = len(registry.get('images', {}))
        print(f"✅ Registry System: ACTIVE")
        print(f"   📝 Poems in registry: {poems_count}")
        print(f"   🖼️  Images in registry: {images_count}")
    else:
        print(f"❌ Registry System: NOT INITIALIZED")
        print(f"   💡 Run 'python3 poetry_manager.py' to set up")
    
    # Count current files
    print(f"\n📁 Current File Structure:")
    
    # Count poems by directory
    poetry_dirs = [
        'Poetry/by_language/english/lengths/short/',
        'Poetry/by_language/english/forms/free_verse/',
        'Poetry/by_language/english/forms/sonnet/',
        'Poetry/by_language/hindi/lengths/standard/'
    ]
    
    total_poems = 0
    for dir_path in poetry_dirs:
        if os.path.exists(dir_path):
            count = len(glob.glob(os.path.join(dir_path, "*.md")))
            total_poems += count
            category = dir_path.split('/')[-2] if dir_path.endswith('/') else dir_path.split('/')[-1]
            print(f"   📚 {category}: {count} poems")
    
    # Count images
    image_dir = 'assets/images/poems/'
    if os.path.exists(image_dir):
        image_count = len(glob.glob(os.path.join(image_dir, "*.png")))
        print(f"   🖼️  Images: {image_count} files")
    else:
        image_count = 0
        print(f"   🖼️  Images: Directory not found")
    
    print(f"\n📊 Collection Overview:")
    print(f"   Total Poems: {total_poems}")
    print(f"   Total Images: {image_count}")
    
    # Check migration status
    print(f"\n🚀 Migration Status:")
    
    # Check if any ID-based files exist
    id_based_poems = len(glob.glob('Poetry/poem*.md'))
    if id_based_poems > 0:
        print(f"   ✅ ID-Based System: ACTIVE ({id_based_poems} poems)")
        print(f"   📁 Files organized as: poem001.md, poem002.md, etc.")
    else:
        print(f"   ❌ ID-Based System: NOT MIGRATED")
        print(f"   📁 Files still use title-based names")
    
    # Check JavaScript files
    print(f"\n📜 JavaScript Status:")
    js_files = ['js/content-loader.js', 'js/dynamic-poem-loader.js']
    for js_file in js_files:
        if os.path.exists(js_file):
            with open(js_file, 'r') as f:
                content = f.read()
                if 'poem001.md' in content or 'Poetry/poem' in content:
                    print(f"   ✅ {js_file}: Updated for ID-based system")
                else:
                    print(f"   ⚠️  {js_file}: Still uses title-based paths")
        else:
            print(f"   ❌ {js_file}: Not found")
    
    # Check backups
    print(f"\n💾 Backup Status:")
    backup_dirs = [d for d in os.listdir('.') if d.startswith('backup_') and os.path.isdir(d)]
    if backup_dirs:
        print(f"   ✅ Backups available: {len(backup_dirs)}")
        latest_backup = max(backup_dirs)
        print(f"   📅 Latest: {latest_backup}")
    else:
        print(f"   ❌ No backups found")
    
    # Recommendations
    print(f"\n💡 Recommended Next Steps:")
    
    if not registry_exists:
        print(f"   1. 🎯 Initialize registry: python3 poetry_manager.py")
        print(f"      → Choose 'Migration Operations' → 'Generate Registry'")
        print(f"   2. 🖼️  Assign images: Use 'Image Management' menu")
        print(f"   3. 🚀 Consider migration: Convert to ID-based system")
    elif id_based_poems == 0:
        print(f"   1. 🖼️  Complete image assignments if needed")
        print(f"   2. 🚀 Migrate to ID-based system for better management")
        print(f"   3. 🔍 Run validation after migration")
    else:
        print(f"   ✅ System is fully set up!")
        print(f"   1. 🔍 Run periodic validations")
        print(f"   2. 🖼️  Manage image assignments as needed")
        print(f"   3. 📊 Use bulk operations for content management")
    
    print(f"\n🛠️  Available Tools:")
    print(f"   📋 Quick Status: python3 status_summary.py")
    print(f"   🧪 Test System: python3 test_poetry_manager.py")
    print(f"   🎭 Full Manager: python3 poetry_manager.py")
    print(f"   📖 Documentation: POETRY_MANAGER_README.md")

if __name__ == "__main__":
    main()