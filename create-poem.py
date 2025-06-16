#!/usr/bin/env python3
"""
Simple Poem Creator - Just run this script to add a new poem easily!
"""
import os
import re
from datetime import datetime

def clean_filename(text):
    """Convert title to safe filename"""
    # Remove special characters, keep only letters, numbers, spaces, hyphens
    clean = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces with hyphens and convert to lowercase
    clean = re.sub(r'\s+', '-', clean.strip()).lower()
    return clean

def get_first_line(content):
    """Extract first line for filename"""
    lines = content.strip().split('\n')
    first_line = lines[0] if lines else "untitled"
    return clean_filename(first_line)[:30]  # Limit length

def create_poem():
    print("🎭 Simple Poem Creator")
    print("=" * 40)
    
    # Get poem details
    title = input("📝 Poem Title: ").strip()
    if not title:
        print("❌ Title is required!")
        return
    
    author = input("👤 Author (default: Manas Pandey): ").strip()
    if not author:
        author = "Manas Pandey"
    
    print("\n📚 Poem Categories:")
    print("1. Short poems")
    print("2. Free verse poems")
    print("3. Sonnets")
    print("4. Hindi poems")
    
    category = input("Choose category (1-4): ").strip()
    
    # Map category to directory and form
    category_map = {
        '1': ('Poetry/by_language/english/lengths/short', 'short', 'short', 'en'),
        '2': ('Poetry/by_language/english/forms/free_verse', 'free_verse', 'standard', 'en'),
        '3': ('Poetry/by_language/english/forms/sonnet', 'sonnet', 'standard', 'en'),
        '4': ('Poetry/by_language/hindi/lengths/standard', 'free_verse', 'standard', 'hi')
    }
    
    if category not in category_map:
        print("❌ Invalid category!")
        return
    
    directory, form, length, language = category_map[category]
    
    print(f"\n📝 Enter your poem content (press Enter twice when done):")
    content_lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line.strip() == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
        content_lines.append(line)
    
    content = '\n'.join(content_lines).strip()
    if not content:
        print("❌ Poem content is required!")
        return
    
    # Ask about image
    image_name = input("\n🖼️  Image filename (e.g., 'my-poem.png') or press Enter to skip: ").strip()
    
    # Generate filename
    title_clean = clean_filename(title)
    first_line_clean = get_first_line(content)
    filename = f"{title_clean}_{first_line_clean}_{length}_{language}.md"
    
    # Create full path
    full_directory = directory
    full_path = os.path.join(full_directory, filename)
    
    # Create directory if it doesn't exist
    os.makedirs(full_directory, exist_ok=True)
    
    # Create poem content
    poem_content = f"""---
title: "{title}"
author: "{author}"
original_path: "{full_path}"
language: "{language}"
form: "{form}"
length: "{length}"
image: "{image_name}"
---
{content}"""
    
    # Write file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(poem_content)
    
    print(f"\n✅ Poem created successfully!")
    print(f"📁 File: {full_path}")
    
    if image_name:
        print(f"🖼️  Don't forget to add your image: assets/images/poems/{image_name}")
    
    print(f"\n🚀 Next steps:")
    print(f"1. {'Add your image to assets/images/poems/' if image_name else 'Optionally add an image to assets/images/poems/'}")
    print(f"2. Commit and push to GitHub")
    print(f"3. Your poem will appear on the website automatically!")

if __name__ == "__main__":
    try:
        create_poem()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")