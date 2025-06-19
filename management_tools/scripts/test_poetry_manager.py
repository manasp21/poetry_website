#!/usr/bin/env python3
"""
Test script for Poetry Manager - Demonstrates basic functionality
"""

import sys
import os
from poetry_manager import PoemRegistry, PoemMigrator, ValidationTools, ImageManager

def main():
    print("🧪 Poetry Manager Test Script")
    print("=" * 40)
    
    # Initialize components
    registry = PoemRegistry()
    migrator = PoemMigrator(registry)
    validator = ValidationTools(registry)
    image_manager = ImageManager(registry)
    
    print(f"📊 Current Status:")
    print(f"   Registry file exists: {'✅' if os.path.exists('poem_registry.json') else '❌'}")
    print(f"   Poems in registry: {len(registry.registry['poems'])}")
    print(f"   Images in registry: {len(registry.registry['images'])}")
    
    if len(registry.registry["poems"]) == 0:
        print("\n🔍 No poems found in registry. Running structure analysis...")
        analysis = migrator.analyze_current_structure()
        
        print(f"\n📈 Analysis Results:")
        print(f"   Total poems found: {analysis['total_poems']}")
        print(f"   Total images found: {analysis['total_images']}")
        print(f"   Poems without images: {len(analysis['poems_without_images'])}")
        print(f"   Orphaned images: {len(analysis['orphaned_images'])}")
        
        print(f"\n💡 To proceed with migration:")
        print(f"   1. Run: python3 poetry_manager.py")
        print(f"   2. Choose 'Migration Operations' -> 'Generate Registry from Current Files'")
        print(f"   3. Then perform full migration when ready")
    else:
        print("\n✅ Registry loaded! Running validation...")
        issues = validator.validate_registry_integrity()
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        
        if total_issues == 0:
            print("✅ All validation checks passed!")
        else:
            print(f"⚠️  Found {total_issues} issues that need attention")
        
        # Show image assignment status
        unassigned_images = image_manager.list_unassigned_images()
        poems_without_images = image_manager.list_poems_without_images()
        
        print(f"\n🖼️ Image Assignment Status:")
        print(f"   Unassigned images: {len(unassigned_images)}")
        print(f"   Poems without images: {len(poems_without_images)}")
        
        if unassigned_images and poems_without_images:
            suggestions = image_manager.auto_suggest_image_assignments()
            print(f"   Auto-suggestions available: {len(suggestions)}")

if __name__ == "__main__":
    main()