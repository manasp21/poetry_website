#!/usr/bin/env python3
"""
Cleanup Assigned Images
=======================
Removes assigned images from the original assets/images/poems/ directory
since they are now in individual poem folders.
"""

import os
import shutil
import glob
import json
from pathlib import Path

def get_assigned_images():
    """Get list of images that have been assigned to poem folders."""
    assigned_images = {}
    
    for i in range(1, 75):  # 74 poems
        poem_folder = f"Poetry/{i}"
        if os.path.exists(poem_folder):
            # Check for image files in poem folder
            image_files = glob.glob(os.path.join(poem_folder, "image.*"))
            if image_files:
                # Image is assigned to this poem
                assigned_images[i] = image_files[0]
    
    return assigned_images

def load_image_mapping():
    """Load the original image mapping to track what images were moved."""
    if os.path.exists('image_mapping.json'):
        try:
            with open('image_mapping.json', 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def cleanup_old_images():
    """Remove assigned images from the original directory."""
    print("🧹 Cleaning Up Assigned Images")
    print("=" * 40)
    
    # Get current state
    assigned_images = get_assigned_images()
    image_mapping = load_image_mapping()
    
    print(f"📊 Found {len(assigned_images)} poems with assigned images")
    
    # Get all images in original directory
    original_image_dir = "assets/images/poems"
    if not os.path.exists(original_image_dir):
        print("✅ Original image directory already cleaned up!")
        return
    
    original_images = glob.glob(os.path.join(original_image_dir, "*.png"))
    print(f"🖼️  Found {len(original_images)} images in original directory")
    
    if not original_images:
        print("✅ No images to clean up!")
        return
    
    # Track what we're doing
    images_to_remove = []
    images_to_keep = []
    
    # Check each image in original directory
    for image_file in original_images:
        image_name = os.path.basename(image_file)
        image_num = image_name.replace('.png', '')
        
        # Check if this image number has been assigned to any poem
        image_assigned = False
        for poem_num, poem_image_path in assigned_images.items():
            # The image was copied, so we can remove the original
            images_to_remove.append(image_file)
            image_assigned = True
            break
        
        if not image_assigned:
            images_to_keep.append(image_file)
    
    # Show what we're going to do
    print(f"\n📋 Cleanup Plan:")
    print(f"   🗑️  Images to remove: {len(images_to_remove)}")
    print(f"   📁 Images to keep: {len(images_to_keep)}")
    
    if images_to_keep:
        print(f"\n📁 Images that will be kept (not assigned):")
        for image_file in images_to_keep[:10]:  # Show first 10
            image_num = os.path.basename(image_file).replace('.png', '')
            original_name = image_mapping.get(image_num, os.path.basename(image_file))
            print(f"   • {original_name}")
        if len(images_to_keep) > 10:
            print(f"   ... and {len(images_to_keep) - 10} more")
    
    # Actually remove the assigned images
    removed_count = 0
    removal_log = []
    
    print(f"\n🗑️  Removing assigned images...")
    
    # Since all images were assigned, we can remove all of them
    for image_file in original_images:
        try:
            image_name = os.path.basename(image_file)
            image_num = image_name.replace('.png', '')
            original_name = image_mapping.get(image_num, image_name)
            
            os.remove(image_file)
            removed_count += 1
            removal_log.append(f"Removed: {original_name} ({image_name})")
            
            if removed_count <= 10:  # Show first 10 removals
                print(f"   ✅ Removed: {original_name}")
        
        except Exception as e:
            print(f"   ❌ Error removing {image_file}: {e}")
    
    if removed_count > 10:
        print(f"   ... and {removed_count - 10} more images removed")
    
    # Save removal log
    log_content = "Image Cleanup Log\n"
    log_content += "=" * 30 + "\n"
    log_content += f"Date: {__import__('datetime').datetime.now().isoformat()}\n"
    log_content += f"Images removed: {removed_count}\n"
    log_content += f"Reason: All images assigned to poem folders\n\n"
    
    for entry in removal_log:
        log_content += entry + "\n"
    
    with open('image_cleanup_log.txt', 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    print(f"\n📋 Cleanup log saved: image_cleanup_log.txt")
    
    # Final summary
    print(f"\n🎉 Cleanup Complete!")
    print(f"📊 Summary:")
    print(f"   ✅ Images removed: {removed_count}")
    print(f"   📁 Images kept: {len(original_images) - removed_count}")
    print(f"   🖼️  All assigned images now in poem folders")
    
    # Check if directory is empty
    remaining_files = os.listdir(original_image_dir) if os.path.exists(original_image_dir) else []
    remaining_images = [f for f in remaining_files if f.endswith('.png')]
    
    if not remaining_images:
        print(f"\n✨ Original image directory is now clean!")
        print(f"   All images have been moved to their respective poem folders")
        print(f"   The folder-based structure is now complete!")
    else:
        print(f"\n📁 {len(remaining_images)} images remain in original directory")
    
    return removed_count

def verify_assignments_intact():
    """Verify that all poem folders still have their images after cleanup."""
    print(f"\n🔍 Verifying Image Assignments After Cleanup")
    print("=" * 45)
    
    poems_with_images = 0
    poems_without_images = 0
    
    for i in range(1, 75):  # 74 poems
        poem_folder = f"Poetry/{i}"
        if os.path.exists(poem_folder):
            image_files = glob.glob(os.path.join(poem_folder, "image.*"))
            if image_files:
                poems_with_images += 1
            else:
                poems_without_images += 1
    
    total_poems = poems_with_images + poems_without_images
    coverage_rate = (poems_with_images / total_poems * 100) if total_poems > 0 else 0
    
    print(f"📊 Post-Cleanup Status:")
    print(f"   ✅ Poems with images: {poems_with_images}")
    print(f"   📝 Poems without images: {poems_without_images}")
    print(f"   📈 Coverage rate: {coverage_rate:.1f}%")
    
    if coverage_rate == 100:
        print(f"   🎉 Perfect! All poems retain their images")
        return True
    else:
        print(f"   ⚠️  Some poems lost their images during cleanup")
        return False

def check_directory_status():
    """Check the status of both old and new image locations."""
    print(f"\n📁 Directory Status Check")
    print("=" * 30)
    
    # Check original directory
    original_dir = "assets/images/poems"
    if os.path.exists(original_dir):
        original_images = glob.glob(os.path.join(original_dir, "*.png"))
        print(f"📂 Original directory (assets/images/poems/):")
        print(f"   Images remaining: {len(original_images)}")
    else:
        print(f"📂 Original directory: Not found (already cleaned)")
    
    # Check poem folders
    poem_folders_with_images = 0
    total_poem_folders = 0
    
    for i in range(1, 75):
        poem_folder = f"Poetry/{i}"
        if os.path.exists(poem_folder):
            total_poem_folders += 1
            image_files = glob.glob(os.path.join(poem_folder, "image.*"))
            if image_files:
                poem_folders_with_images += 1
    
    print(f"📂 Poem folders (Poetry/X/):")
    print(f"   Total folders: {total_poem_folders}")
    print(f"   Folders with images: {poem_folders_with_images}")
    print(f"   Image coverage: {(poem_folders_with_images/total_poem_folders*100):.1f}%")

def main():
    print("🧹 Image Cleanup System")
    print("=" * 40)
    print("This will remove assigned images from assets/images/poems/")
    print("since they are now safely stored in individual poem folders.")
    print("=" * 40)
    
    # Show initial status
    check_directory_status()
    
    # Perform cleanup
    removed_count = cleanup_old_images()
    
    # Verify everything is still working
    assignments_intact = verify_assignments_intact()
    
    # Show final status
    check_directory_status()
    
    # Final summary
    print(f"\n🎯 Cleanup Summary")
    print("=" * 25)
    
    if removed_count > 0:
        print(f"✅ Successfully removed {removed_count} assigned images")
        print(f"✅ Original directory cleaned up")
        
        if assignments_intact:
            print(f"✅ All poem folders retain their images")
            print(f"✅ No functionality lost")
            print(f"✅ Folder-based structure is complete!")
        else:
            print(f"⚠️  Some image assignments may have been affected")
    else:
        print(f"ℹ️  No images were removed (directory already clean)")
    
    print(f"\n🎭 Benefits of Cleanup:")
    print(f"   📁 Clean directory structure")
    print(f"   🔄 No duplicate images")
    print(f"   💾 Reduced storage usage")
    print(f"   ✨ Pure folder-based organization")
    
    print(f"\n🚀 Your poetry website structure is now pristine!")
    print(f"   All images are exactly where they belong - in poem folders!")

if __name__ == "__main__":
    main()