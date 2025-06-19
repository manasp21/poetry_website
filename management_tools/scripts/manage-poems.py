#!/usr/bin/env python3
"""
Simple Poem Manager - List, edit, and manage your poems easily!
"""
import os
import glob
from pathlib import Path

def find_all_poems():
    """Find all poem files in the repository"""
    poem_dirs = [
        'Poetry/by_language/english/lengths/short/',
        'Poetry/by_language/english/forms/free_verse/',
        'Poetry/by_language/english/forms/sonnet/',
        'Poetry/by_language/hindi/lengths/standard/'
    ]
    
    poems = []
    for poem_dir in poem_dirs:
        if os.path.exists(poem_dir):
            for file_path in glob.glob(os.path.join(poem_dir, "*.md")):
                poems.append({
                    'path': file_path,
                    'name': os.path.basename(file_path),
                    'category': poem_dir.split('/')[-2] if 'forms' in poem_dir else poem_dir.split('/')[-1]
                })
    
    return sorted(poems, key=lambda x: x['name'])

def read_poem_metadata(file_path):
    """Extract title and basic info from poem file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from frontmatter
        lines = content.split('\n')
        title = "Unknown Title"
        author = "Unknown Author"
        
        for line in lines:
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('author:'):
                author = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('---') and lines.index(line) > 0:
                break
        
        return title, author
    except:
        return "Error reading file", "Unknown"

def list_poems():
    """List all poems with numbers for easy selection"""
    poems = find_all_poems()
    
    if not poems:
        print("📝 No poems found!")
        return []
    
    print(f"\n📚 Found {len(poems)} poems:")
    print("=" * 60)
    
    for i, poem in enumerate(poems, 1):
        title, author = read_poem_metadata(poem['path'])
        category = poem['category'].replace('_', ' ').title()
        print(f"{i:2d}. {title}")
        print(f"    👤 {author} | 📁 {category}")
        print(f"    📄 {poem['path']}")
        print()
    
    return poems

def edit_poem(poems):
    """Edit a selected poem"""
    if not poems:
        return
    
    try:
        choice = int(input("Enter poem number to edit: "))
        if 1 <= choice <= len(poems):
            poem_path = poems[choice - 1]['path']
            print(f"\n📝 Opening {poem_path}")
            
            # Try different editors
            editors = ['code', 'notepad', 'nano', 'vim']
            for editor in editors:
                try:
                    os.system(f'{editor} "{poem_path}"')
                    break
                except:
                    continue
            else:
                print(f"📁 Please manually edit: {poem_path}")
        else:
            print("❌ Invalid poem number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_poem(poems):
    """Delete a selected poem"""
    if not poems:
        return
    
    try:
        choice = int(input("Enter poem number to DELETE: "))
        if 1 <= choice <= len(poems):
            poem_path = poems[choice - 1]['path']
            title, author = read_poem_metadata(poem_path)
            
            print(f"\n⚠️  You are about to DELETE:")
            print(f"   Title: {title}")
            print(f"   File: {poem_path}")
            
            confirm = input("\nType 'DELETE' to confirm: ").strip()
            if confirm == 'DELETE':
                os.remove(poem_path)
                print(f"✅ Poem deleted: {poem_path}")
            else:
                print("❌ Deletion cancelled")
        else:
            print("❌ Invalid poem number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def check_images():
    """Check which poems have images and which don't"""
    poems = find_all_poems()
    image_dir = Path("assets/images/poems")
    
    if not image_dir.exists():
        print("❌ Images directory not found!")
        return
    
    print("\n🖼️  Image Status Report:")
    print("=" * 50)
    
    has_image = []
    no_image = []
    
    for poem in poems:
        title, author = read_poem_metadata(poem['path'])
        
        # Check if image exists
        with open(poem['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        image_name = ""
        for line in content.split('\n'):
            if line.startswith('image:'):
                image_name = line.split(':', 1)[1].strip().strip('"\'')
                break
        
        if image_name and image_name != "":
            image_path = image_dir / image_name
            if image_path.exists():
                has_image.append((title, image_name))
            else:
                no_image.append((title, f"Missing: {image_name}"))
        else:
            no_image.append((title, "No image specified"))
    
    print(f"✅ Poems with images ({len(has_image)}):")
    for title, img in has_image:
        print(f"   • {title} → {img}")
    
    print(f"\n❌ Poems without images ({len(no_image)}):")
    for title, status in no_image:
        print(f"   • {title} → {status}")

def main_menu():
    """Main menu for poem management"""
    while True:
        print("\n🎭 Simple Poem Manager")
        print("=" * 30)
        print("1. List all poems")
        print("2. Edit a poem")
        print("3. Delete a poem")
        print("4. Check image status")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            list_poems()
        elif choice == '2':
            poems = list_poems()
            edit_poem(poems)
        elif choice == '3':
            poems = list_poems()
            delete_poem(poems)
        elif choice == '4':
            check_images()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")