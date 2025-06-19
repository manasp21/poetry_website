#!/usr/bin/env python3
"""
Random Image Assignment
=======================
Randomly assigns all unassigned images to poem folders that don't have images.
"""

import os
import random
import shutil
import glob
from pathlib import Path

def get_poems_without_images():
    """Get list of poem folders that don't have images."""
    poems_without_images = []
    
    for i in range(1, 75):  # 74 poems total
        poem_folder = f"Poetry/{i}"
        if os.path.exists(poem_folder):
            # Check if image exists in folder
            image_files = glob.glob(os.path.join(poem_folder, "image.*"))
            if not image_files:
                poems_without_images.append(i)
    
    return poems_without_images

def get_unassigned_images():
    """Get list of images still in the original location."""
    unassigned_images = []
    image_dir = "assets/images/poems"
    
    if os.path.exists(image_dir):
        for image_file in glob.glob(os.path.join(image_dir, "*.png")):
            unassigned_images.append(image_file)
    
    return unassigned_images

def get_poem_title(poem_num):
    """Get poem title for display purposes."""
    poem_file = f"Poetry/{poem_num}/poem.md"
    if os.path.exists(poem_file):
        try:
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from frontmatter
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"\'')
                    return title
        except Exception:
            pass
    return f"Poem {poem_num}"

def load_image_mapping():
    """Load original image names from mapping file."""
    image_mapping = {}
    if os.path.exists('image_mapping.json'):
        try:
            import json
            with open('image_mapping.json', 'r') as f:
                image_mapping = json.load(f)
        except Exception:
            pass
    return image_mapping

def random_assign_images():
    """Randomly assign unassigned images to poems without images."""
    print("🎲 Random Image Assignment")
    print("=" * 40)
    
    # Get poems without images and unassigned images
    poems_without_images = get_poems_without_images()
    unassigned_images = get_unassigned_images()
    image_mapping = load_image_mapping()
    
    print(f"📝 Found {len(poems_without_images)} poems without images")
    print(f"🖼️  Found {len(unassigned_images)} unassigned images")
    
    if not poems_without_images:
        print("✅ All poems already have images!")
        return
    
    if not unassigned_images:
        print("✅ No unassigned images to distribute!")
        return
    
    # Shuffle both lists for randomness
    random.shuffle(poems_without_images)
    random.shuffle(unassigned_images)
    
    # Assign images randomly
    assignments = []
    assigned_count = 0
    
    for i, image_file in enumerate(unassigned_images):
        if i >= len(poems_without_images):
            break  # More images than poems without images
        
        poem_num = poems_without_images[i]
        poem_folder = f"Poetry/{poem_num}"
        dest_image = os.path.join(poem_folder, "image.png")
        
        try:
            # Copy image to poem folder
            shutil.copy2(image_file, dest_image)
            
            # Get original image name for display
            image_num = os.path.basename(image_file).replace('.png', '')
            original_name = image_mapping.get(image_num, os.path.basename(image_file))
            
            # Get poem title
            poem_title = get_poem_title(poem_num)
            
            assignments.append({
                'poem_num': poem_num,
                'poem_title': poem_title,
                'image_file': image_file,
                'original_name': original_name
            })
            
            assigned_count += 1
            print(f"✅ Assigned {original_name} → Poem {poem_num} ({poem_title})")
            
        except Exception as e:
            print(f"❌ Error assigning {image_file} to poem {poem_num}: {e}")
    
    print(f"\n🎉 Random Assignment Complete!")
    print(f"📊 Successfully assigned {assigned_count} images")
    
    # Show statistics
    remaining_poems = len(poems_without_images) - assigned_count
    remaining_images = len(unassigned_images) - assigned_count
    
    if remaining_poems > 0:
        print(f"📝 {remaining_poems} poems still without images")
    
    if remaining_images > 0:
        print(f"🖼️  {remaining_images} images still unassigned")
    
    # Save assignment log
    save_assignment_log(assignments)
    
    return assignments

def save_assignment_log(assignments):
    """Save the assignment log for reference."""
    log_content = "Random Image Assignment Log\n"
    log_content += "=" * 40 + "\n"
    log_content += f"Date: {__import__('datetime').datetime.now().isoformat()}\n"
    log_content += f"Total assignments: {len(assignments)}\n\n"
    
    for assignment in assignments:
        log_content += f"Poem {assignment['poem_num']}: {assignment['poem_title']}\n"
        log_content += f"  ← {assignment['original_name']}\n"
        log_content += f"  Source: {assignment['image_file']}\n\n"
    
    with open('random_assignment_log.txt', 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    print(f"📋 Assignment log saved: random_assignment_log.txt")

def show_before_after_stats():
    """Show before and after statistics."""
    print(f"\n📊 Before Assignment:")
    
    poems_without_images = get_poems_without_images()
    unassigned_images = get_unassigned_images()
    
    print(f"   📝 Poems without images: {len(poems_without_images)}")
    print(f"   🖼️  Unassigned images: {len(unassigned_images)}")
    
    return len(poems_without_images), len(unassigned_images)

def show_final_stats(initial_poems_without, initial_unassigned):
    """Show final statistics after assignment."""
    print(f"\n📊 After Assignment:")
    
    poems_without_images = get_poems_without_images()
    unassigned_images = get_unassigned_images()
    
    print(f"   📝 Poems without images: {len(poems_without_images)}")
    print(f"   🖼️  Unassigned images: {len(unassigned_images)}")
    
    # Calculate what was assigned
    assigned_poems = initial_poems_without - len(poems_without_images)
    assigned_images = initial_unassigned - len(unassigned_images)
    
    print(f"\n🎯 Assignment Results:")
    print(f"   ✅ Poems gained images: {assigned_poems}")
    print(f"   ✅ Images assigned: {assigned_images}")
    
    # Calculate total image coverage
    total_poems = 74
    poems_with_images = total_poems - len(poems_without_images)
    coverage_rate = (poems_with_images / total_poems) * 100
    
    print(f"\n📈 Total Image Coverage:")
    print(f"   🖼️  Poems with images: {poems_with_images}/{total_poems}")
    print(f"   📊 Coverage rate: {coverage_rate:.1f}%")

def main():
    print("🎲 Random Image Assignment System")
    print("=" * 50)
    print("This will randomly assign all unassigned images to poems")
    print("that don't currently have images.")
    print("=" * 50)
    
    # Show initial statistics
    initial_poems_without, initial_unassigned = show_before_after_stats()
    
    if initial_poems_without == 0:
        print("\n✅ All poems already have images! Nothing to assign.")
        return
    
    if initial_unassigned == 0:
        print("\n✅ No unassigned images found! All images are already in use.")
        return
    
    print(f"\n🎯 Will assign up to {min(initial_poems_without, initial_unassigned)} images")
    
    # Perform random assignment
    assignments = random_assign_images()
    
    if assignments:
        # Show final statistics
        show_final_stats(initial_poems_without, initial_unassigned)
        
        print(f"\n🎭 Random Assignment Benefits:")
        print("   🎲 Creates diverse visual combinations")
        print("   ⚡ Instant completion of image assignments")
        print("   🔄 Images automatically detected by website")
        print("   ✨ No manual configuration needed")
        
        print(f"\n🌐 Website Impact:")
        print("   📝 More poems now display with images")
        print("   🎨 Improved visual appeal")
        print("   📊 Better user engagement")
        print("   🚀 Ready for deployment!")
    
    print(f"\n🎉 Random assignment complete!")
    print("Your poetry website now has maximum visual impact! 🎭✨")

if __name__ == "__main__":
    main()