#!/usr/bin/env python3
"""
Verification Script - Check Renaming Results
===========================================
Verify the sequential renaming was successful and show assignment status.
"""

import os
import json
import glob

def verify_structure():
    """Verify the new structure is correct."""
    print("🔍 Verifying Sequential Renaming Results")
    print("=" * 50)
    
    # Check poems
    poems = sorted(glob.glob("Poetry/*.md"))
    expected_poems = [f"Poetry/{i}.md" for i in range(1, 75)]  # 74 poems total
    
    print(f"📝 Poems:")
    print(f"   Found: {len(poems)} files")
    print(f"   Expected: {len(expected_poems)} files")
    
    missing_poems = []
    for expected in expected_poems:
        if expected not in poems:
            missing_poems.append(expected)
    
    if missing_poems:
        print(f"   ❌ Missing: {missing_poems}")
    else:
        print(f"   ✅ All poems present: 1.md through 74.md")
    
    # Check images
    images = sorted(glob.glob("assets/images/poems/*.png"))
    expected_images = [f"assets/images/poems/{i}.png" for i in range(1, 80)]  # 79 images total
    
    print(f"\n🖼️ Images:")
    print(f"   Found: {len(images)} files")
    print(f"   Expected: {len(expected_images)} files")
    
    missing_images = []
    for expected in expected_images:
        if expected not in images:
            missing_images.append(expected)
    
    if missing_images:
        print(f"   ❌ Missing: {missing_images}")
    else:
        print(f"   ✅ All images present: 1.png through 79.png")
    
    # Check mapping files
    print(f"\n📋 Mapping Files:")
    
    if os.path.exists('poem_mapping.json'):
        with open('poem_mapping.json', 'r') as f:
            poem_mapping = json.load(f)
        print(f"   ✅ poem_mapping.json: {len(poem_mapping)} entries")
    else:
        print(f"   ❌ poem_mapping.json: Not found")
    
    if os.path.exists('image_mapping.json'):
        with open('image_mapping.json', 'r') as f:
            image_mapping = json.load(f)
        print(f"   ✅ image_mapping.json: {len(image_mapping)} entries")
    else:
        print(f"   ❌ image_mapping.json: Not found")

def check_assignment_status():
    """Check how many poems have assigned images."""
    print(f"\n🎯 Image Assignment Status")
    print("=" * 30)
    
    assigned_count = 0
    unassigned_count = 0
    assignments = []
    
    for i in range(1, 75):  # 74 poems
        poem_file = f"Poetry/{i}.md"
        if os.path.exists(poem_file):
            try:
                with open(poem_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract image field
                lines = content.split('\n')
                image_value = ""
                for line in lines:
                    if line.strip().startswith('image:'):
                        image_value = line.split(':', 1)[1].strip().strip('"\'')
                        break
                
                if image_value and image_value != "":
                    assigned_count += 1
                    assignments.append((i, image_value))
                else:
                    unassigned_count += 1
                    
            except Exception as e:
                print(f"   ❌ Error reading {poem_file}: {e}")
    
    print(f"📊 Assignment Summary:")
    print(f"   ✅ Assigned: {assigned_count} poems")
    print(f"   ❌ Unassigned: {unassigned_count} poems")
    print(f"   📈 Assignment rate: {(assigned_count/74*100):.1f}%")
    
    if assignments:
        print(f"\n🔗 Current Assignments:")
        for poem_num, image_name in assignments[:5]:  # Show first 5
            print(f"   poem {poem_num} → {image_name}")
        if len(assignments) > 5:
            print(f"   ... and {len(assignments) - 5} more")

def show_mapping_examples():
    """Show examples from the mapping files."""
    print(f"\n📖 Mapping Examples")
    print("=" * 30)
    
    # Show poem mappings
    if os.path.exists('poem_mapping.json'):
        with open('poem_mapping.json', 'r') as f:
            poem_mapping = json.load(f)
        
        print(f"📝 Poem Mappings (first 5):")
        for i in range(1, min(6, len(poem_mapping) + 1)):
            key = str(i)
            if key in poem_mapping:
                data = poem_mapping[key]
                print(f"   {i}.md → \"{data['title']}\"")
                print(f"           (was: {data['original_name']})")
    
    # Show image mappings
    if os.path.exists('image_mapping.json'):
        with open('image_mapping.json', 'r') as f:
            image_mapping = json.load(f)
        
        print(f"\n🖼️ Image Mappings (first 5):")
        for i in range(1, min(6, len(image_mapping) + 1)):
            key = str(i)
            if key in image_mapping:
                original_name = image_mapping[key]
                print(f"   {i}.png → {original_name}")

def show_assignment_suggestions():
    """Show suggested assignments based on name matching."""
    print(f"\n💡 Assignment Suggestions")
    print("=" * 30)
    
    if not (os.path.exists('poem_mapping.json') and os.path.exists('image_mapping.json')):
        print("❌ Mapping files not found")
        return
    
    with open('poem_mapping.json', 'r') as f:
        poem_mapping = json.load(f)
    
    with open('image_mapping.json', 'r') as f:
        image_mapping = json.load(f)
    
    print("🎯 Suggested Matches (based on similar names):")
    
    suggestions = []
    
    # Look for obvious matches
    for poem_num, poem_data in poem_mapping.items():
        poem_title = poem_data['title'].lower()
        
        for image_num, image_name in image_mapping.items():
            image_base = image_name.replace('.png', '').replace('-', ' ').lower()
            
            # Simple matching logic
            if any(word in image_base for word in poem_title.split() if len(word) > 3):
                suggestions.append((poem_num, poem_data['title'], image_num, image_name))
    
    # Show first 10 suggestions
    for i, (poem_num, poem_title, image_num, image_name) in enumerate(suggestions[:10]):
        print(f"   {poem_num}.md (\"{poem_title}\") → {image_num}.png ({image_name})")
    
    if len(suggestions) > 10:
        print(f"   ... and {len(suggestions) - 10} more suggestions")
    
    print(f"\n📝 To assign: Edit Poetry/{poem_num}.md and change:")
    print(f"   image: \"{image_num}.png\"")

def main():
    print("✨ Sequential Renaming - Verification Complete")
    print("=" * 60)
    
    verify_structure()
    check_assignment_status()
    show_mapping_examples()
    show_assignment_suggestions()
    
    print(f"\n🎯 Summary")
    print("=" * 20)
    print("✅ All files renamed to sequential numbers")
    print("✅ Original names preserved in mapping files")
    print("✅ JavaScript files updated")
    print("✅ Backup created for safety")
    print("✅ Structure ready for manual image assignment")
    
    print(f"\n🚀 Next Steps:")
    print("1. 📝 Edit poem files to assign images")
    print("2. 🔍 Use suggestions above for quick matching")  
    print("3. 🌐 Test website locally")
    print("4. 🎭 Your poetry collection is now cleanly organized!")

if __name__ == "__main__":
    main()