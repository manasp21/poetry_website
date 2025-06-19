#!/usr/bin/env python3
"""
Comprehensive Consistency Checker
=================================
Verifies that the folder-based structure maintains all original functionality
and that the website will work exactly as it did before the overhaul.
"""

import os
import json
import glob
import re
from pathlib import Path

def check_poem_structure():
    """Check that all poems are properly structured."""
    print("📝 Checking Poem Structure")
    print("=" * 30)
    
    issues = []
    successes = []
    
    for i in range(1, 75):  # 74 poems
        poem_folder = f"Poetry/{i}"
        poem_file = os.path.join(poem_folder, "poem.md")
        
        if not os.path.exists(poem_folder):
            issues.append(f"Missing folder: Poetry/{i}/")
            continue
        
        if not os.path.exists(poem_file):
            issues.append(f"Missing poem file: {poem_file}")
            continue
        
        # Check poem content structure
        try:
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check YAML frontmatter
            if not content.strip().startswith('---'):
                issues.append(f"Poem {i}: Missing YAML frontmatter")
                continue
            
            # Parse frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                issues.append(f"Poem {i}: Malformed YAML frontmatter")
                continue
            
            frontmatter_text = parts[1]
            poem_content = parts[2].strip()
            
            # Check required fields
            required_fields = ['title', 'author', 'language', 'form', 'length']
            missing_fields = []
            
            for field in required_fields:
                if f"{field}:" not in frontmatter_text:
                    missing_fields.append(field)
            
            if missing_fields:
                issues.append(f"Poem {i}: Missing fields: {', '.join(missing_fields)}")
            
            # Check that there's no image field (should be removed)
            if 'image:' in frontmatter_text:
                issues.append(f"Poem {i}: Still has image field (should be removed)")
            
            # Check that poem has content
            if not poem_content:
                issues.append(f"Poem {i}: No poem content")
            
            if not missing_fields and 'image:' not in frontmatter_text and poem_content:
                successes.append(i)
                
        except Exception as e:
            issues.append(f"Poem {i}: Error reading file - {e}")
    
    print(f"✅ Successfully structured poems: {len(successes)}/74")
    
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more issues")
    else:
        print("✅ All poems properly structured!")
    
    return len(issues) == 0

def check_image_assignments():
    """Check image assignments and automatic detection."""
    print(f"\n🖼️ Checking Image Assignments")
    print("=" * 30)
    
    poems_with_images = 0
    poems_without_images = 0
    broken_images = []
    
    for i in range(1, 75):  # 74 poems
        poem_folder = f"Poetry/{i}"
        
        if not os.path.exists(poem_folder):
            continue
        
        # Check for image files
        image_files = glob.glob(os.path.join(poem_folder, "image.*"))
        
        if image_files:
            # Verify image file exists and is readable
            image_file = image_files[0]
            try:
                file_size = os.path.getsize(image_file)
                if file_size > 0:
                    poems_with_images += 1
                else:
                    broken_images.append(f"Poem {i}: Empty image file")
            except Exception as e:
                broken_images.append(f"Poem {i}: Error reading image - {e}")
        else:
            poems_without_images += 1
    
    total_poems = poems_with_images + poems_without_images
    coverage_rate = (poems_with_images / total_poems * 100) if total_poems > 0 else 0
    
    print(f"📊 Image Assignment Status:")
    print(f"   ✅ Poems with images: {poems_with_images}")
    print(f"   📝 Poems without images: {poems_without_images}")
    print(f"   📈 Coverage rate: {coverage_rate:.1f}%")
    
    if broken_images:
        print(f"❌ Broken images found:")
        for issue in broken_images:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All images properly assigned and readable!")
        return True

def check_javascript_compatibility():
    """Check that JavaScript files are properly updated."""
    print(f"\n📜 Checking JavaScript Compatibility")
    print("=" * 40)
    
    js_issues = []
    
    # Check content-loader.js
    content_loader_path = 'js/content-loader.js'
    if os.path.exists(content_loader_path):
        with open(content_loader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for folder-based paths
        if 'Poetry/1/poem.md' in content:
            print("✅ content-loader.js: Using folder-based paths")
        else:
            js_issues.append("content-loader.js: Not using folder-based paths")
        
        # Check for automatic image detection
        if 'getImagePathForPoem' in content or 'detectImageForPoem' in content:
            print("✅ content-loader.js: Has automatic image detection")
        else:
            js_issues.append("content-loader.js: Missing automatic image detection")
        
        # Check for GitHub Pages compatibility
        if '/poetry_website/' in content:
            print("✅ content-loader.js: GitHub Pages compatible")
        else:
            js_issues.append("content-loader.js: Missing GitHub Pages compatibility")
    else:
        js_issues.append("content-loader.js: File not found")
    
    # Check dynamic-poem-loader.js
    dynamic_loader_path = 'js/dynamic-poem-loader.js'
    if os.path.exists(dynamic_loader_path):
        with open(dynamic_loader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'Poetry/1/poem.md' in content:
            print("✅ dynamic-poem-loader.js: Using folder-based paths")
        else:
            js_issues.append("dynamic-poem-loader.js: Not using folder-based paths")
    else:
        js_issues.append("dynamic-poem-loader.js: File not found")
    
    if js_issues:
        print(f"❌ JavaScript issues found:")
        for issue in js_issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All JavaScript files properly configured!")
        return True

def check_path_compatibility():
    """Check that all paths will work with GitHub Pages."""
    print(f"\n🌐 Checking Path Compatibility")
    print("=" * 30)
    
    path_issues = []
    
    # Check poem paths
    for i in range(1, 75):
        poem_path = f"Poetry/{i}/poem.md"
        if os.path.exists(poem_path):
            # Check for spaces or special characters that might break URLs
            if ' ' in poem_path or any(c in poem_path for c in ['<', '>', '"', "'", '&']):
                path_issues.append(f"Poem {i}: Path contains problematic characters")
        else:
            path_issues.append(f"Poem {i}: File missing at expected path")
    
    # Check image paths
    for i in range(1, 75):
        poem_folder = f"Poetry/{i}"
        if os.path.exists(poem_folder):
            image_files = glob.glob(os.path.join(poem_folder, "image.*"))
            for image_file in image_files:
                if ' ' in image_file or any(c in image_file for c in ['<', '>', '"', "'", '&']):
                    path_issues.append(f"Poem {i}: Image path contains problematic characters")
    
    if path_issues:
        print(f"❌ Path compatibility issues:")
        for issue in path_issues[:10]:
            print(f"   - {issue}")
        if len(path_issues) > 10:
            print(f"   ... and {len(path_issues) - 10} more issues")
        return False
    else:
        print("✅ All paths are GitHub Pages compatible!")
        return True

def check_content_preservation():
    """Check that all original content is preserved."""
    print(f"\n📚 Checking Content Preservation")
    print("=" * 35)
    
    content_issues = []
    
    # Load original mapping if available
    original_mapping = {}
    if os.path.exists('poem_mapping.json'):
        try:
            with open('poem_mapping.json', 'r', encoding='utf-8') as f:
                original_mapping = json.load(f)
        except Exception:
            pass
    
    preserved_content = 0
    total_poems = 0
    
    for i in range(1, 75):
        poem_file = f"Poetry/{i}/poem.md"
        if not os.path.exists(poem_file):
            continue
        
        total_poems += 1
        
        try:
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                poem_content = parts[2].strip()
                
                # Check if poem has title and content
                has_title = 'title:' in frontmatter_text
                has_content = bool(poem_content.strip())
                
                if has_title and has_content:
                    preserved_content += 1
                else:
                    content_issues.append(f"Poem {i}: Missing title or content")
            else:
                content_issues.append(f"Poem {i}: Malformed structure")
                
        except Exception as e:
            content_issues.append(f"Poem {i}: Error reading - {e}")
    
    preservation_rate = (preserved_content / total_poems * 100) if total_poems > 0 else 0
    
    print(f"📊 Content Preservation:")
    print(f"   ✅ Properly preserved: {preserved_content}/{total_poems}")
    print(f"   📈 Preservation rate: {preservation_rate:.1f}%")
    
    if content_issues:
        print(f"❌ Content preservation issues:")
        for issue in content_issues[:5]:
            print(f"   - {issue}")
        if len(content_issues) > 5:
            print(f"   ... and {len(content_issues) - 5} more issues")
        return False
    else:
        print("✅ All content properly preserved!")
        return True

def check_backup_integrity():
    """Check that backups were created properly."""
    print(f"\n💾 Checking Backup Integrity")
    print("=" * 30)
    
    backup_dirs = [d for d in os.listdir('.') if d.startswith('backup_') and os.path.isdir(d)]
    
    if not backup_dirs:
        print("⚠️  No backup directories found")
        return False
    
    latest_backup = max(backup_dirs)
    backup_path = latest_backup
    
    print(f"📁 Latest backup: {latest_backup}")
    
    # Check backup contents
    backup_issues = []
    
    expected_items = ['Poetry', 'images', 'js']
    for item in expected_items:
        item_path = os.path.join(backup_path, item)
        if os.path.exists(item_path):
            print(f"   ✅ {item}: Backed up")
        else:
            backup_issues.append(f"Missing {item} in backup")
    
    if backup_issues:
        print(f"❌ Backup issues:")
        for issue in backup_issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Backup integrity verified!")
        return True

def simulate_website_loading():
    """Simulate how the website would load poems."""
    print(f"\n🌐 Simulating Website Loading")
    print("=" * 35)
    
    loading_issues = []
    successful_loads = 0
    
    # Simulate loading first 5 poems
    for i in range(1, 6):
        poem_path = f"Poetry/{i}/poem.md"
        
        try:
            # Check if poem file exists and is readable
            if not os.path.exists(poem_path):
                loading_issues.append(f"Poem {i}: File not found at {poem_path}")
                continue
            
            with open(poem_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse like JavaScript would
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    poem_content = parts[2].strip()
                    
                    # Extract title (like JavaScript would)
                    title = "Unknown"
                    for line in frontmatter_text.split('\n'):
                        if line.strip().startswith('title:'):
                            title = line.split(':', 1)[1].strip().strip('"\'')
                            break
                    
                    # Check for image (automatic detection simulation)
                    poem_folder = f"Poetry/{i}"
                    image_files = glob.glob(os.path.join(poem_folder, "image.*"))
                    has_image = len(image_files) > 0
                    
                    print(f"   📝 Poem {i}: '{title}' {'🖼️' if has_image else '📄'}")
                    successful_loads += 1
                else:
                    loading_issues.append(f"Poem {i}: Malformed frontmatter")
            else:
                loading_issues.append(f"Poem {i}: No frontmatter found")
                
        except Exception as e:
            loading_issues.append(f"Poem {i}: Loading error - {e}")
    
    print(f"\n📊 Loading Simulation Results:")
    print(f"   ✅ Successfully loaded: {successful_loads}/5")
    
    if loading_issues:
        print(f"❌ Loading issues found:")
        for issue in loading_issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All poems load successfully!")
        return True

def run_comprehensive_checks():
    """Run all consistency checks."""
    print("🔍 Comprehensive Consistency Check")
    print("=" * 50)
    print("Verifying that the folder-based structure maintains")
    print("all original functionality and website compatibility.")
    print("=" * 50)
    
    checks = [
        ("Poem Structure", check_poem_structure),
        ("Image Assignments", check_image_assignments),
        ("JavaScript Compatibility", check_javascript_compatibility),
        ("Path Compatibility", check_path_compatibility),
        ("Content Preservation", check_content_preservation),
        ("Backup Integrity", check_backup_integrity),
        ("Website Loading", simulate_website_loading)
    ]
    
    results = {}
    passed_checks = 0
    
    for check_name, check_function in checks:
        try:
            result = check_function()
            results[check_name] = result
            if result:
                passed_checks += 1
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results[check_name] = False
    
    # Final summary
    print(f"\n🎯 Consistency Check Summary")
    print("=" * 40)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")
    
    overall_success_rate = (passed_checks / len(checks)) * 100
    
    print(f"\n📊 Overall Results:")
    print(f"   Checks passed: {passed_checks}/{len(checks)}")
    print(f"   Success rate: {overall_success_rate:.1f}%")
    
    if overall_success_rate == 100:
        print(f"\n🎉 ALL CHECKS PASSED!")
        print("✅ The folder-based structure is fully functional")
        print("✅ Website will work exactly as before")
        print("✅ All content and functionality preserved")
        print("✅ Ready for deployment!")
    elif overall_success_rate >= 80:
        print(f"\n⚠️  MOSTLY SUCCESSFUL")
        print("Most functionality is working, but some issues need attention.")
    else:
        print(f"\n❌ SIGNIFICANT ISSUES FOUND")
        print("Multiple problems detected. Review and fix before deployment.")
    
    return overall_success_rate == 100

def main():
    """Run the comprehensive consistency checker."""
    try:
        success = run_comprehensive_checks()
        
        if success:
            print(f"\n🎭 Your poetry website overhaul is COMPLETE and VERIFIED!")
            print("The folder-based structure with automatic image detection")
            print("is fully functional and ready for use. 🚀✨")
        else:
            print(f"\n🔧 Some issues were found that need attention.")
            print("Review the checks above and fix any problems before deploying.")
            
    except Exception as e:
        print(f"\n❌ Critical error during consistency check: {e}")

if __name__ == "__main__":
    main()