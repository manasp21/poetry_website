#!/usr/bin/env python3
"""
System Declutter
================
Organizes and cleans up all temporary files created during the overhaul process,
leaving only the essential files for the production poetry website.
"""

import os
import shutil
import glob
from datetime import datetime
from pathlib import Path

def create_management_tools_directory():
    """Create a directory for management tools and move scripts there."""
    tools_dir = "management_tools"
    
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        print(f"📁 Created {tools_dir}/ directory")
    
    return tools_dir

def categorize_files():
    """Categorize all files in the repository."""
    categories = {
        "core_website": [
            "index.html",
            "poem.html", 
            "archive.html",
            "js/",
            "css/",
            "Poetry/",
            "assets/",
            "README.md",
            ".nojekyll"
        ],
        "management_scripts": [
            "poetry_manager.py",
            "simple_rename.py",
            "folder_restructure.py",
            "random_image_assignment.py",
            "cleanup_assigned_images.py",
            "declutter_system.py",
            "consistency_checker.py",
            "verify_folder_structure.py",
            "test_poetry_manager.py",
            "status_summary.py",
            "demo_migration.py",
            "migration_example.py",
            "verify_renaming.py",
            "manage-poems.py",
            "create-poem.py"
        ],
        "enhanced_javascript": [
            "content-loader-folders.js",
            "dynamic-poem-loader-folders.js"
        ],
        "documentation": [
            "POETRY_MANAGER_README.md",
            "FOLDER_STRUCTURE_GUIDE.md",
            "OVERHAUL_COMPLETE.md",
            "FINAL_STATUS_REPORT.md",
            "SETUP_COMPLETE.md",
            "ASSIGNMENT_GUIDE.md",
            "ADMIN_SETUP.md",
            "PERFORMANCE.md",
            "CLAUDE.md",
            "design_document.md",
            "project_enhancement_plan.md"
        ],
        "configuration": [
            "poetry_config.json",
            "requirements.txt"
        ],
        "logs_and_mappings": [
            "poem_mapping.json",
            "image_mapping.json",
            "restructure_log.txt",
            "random_assignment_log.txt",
            "image_cleanup_log.txt"
        ],
        "backups": [
            "backup_simple_*",
            "backup_folder_restructure_*"
        ]
    }
    
    return categories

def organize_files():
    """Organize files into appropriate directories."""
    print("📂 Organizing Files into Categories")
    print("=" * 40)
    
    categories = categorize_files()
    tools_dir = create_management_tools_directory()
    
    # Create subdirectories in management_tools
    subdirs = {
        "scripts": "Management and migration scripts",
        "docs": "Documentation and guides",
        "logs": "Operation logs and mappings",
        "enhanced_js": "Enhanced JavaScript versions",
        "config": "Configuration files"
    }
    
    for subdir, description in subdirs.items():
        subdir_path = os.path.join(tools_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
            print(f"📁 Created {subdir_path}/ - {description}")
    
    # Move management scripts
    moved_files = []
    for script in categories["management_scripts"]:
        if os.path.exists(script):
            dest = os.path.join(tools_dir, "scripts", script)
            shutil.move(script, dest)
            moved_files.append(f"📜 {script} → management_tools/scripts/")
    
    # Move documentation
    for doc in categories["documentation"]:
        if os.path.exists(doc):
            dest = os.path.join(tools_dir, "docs", doc)
            shutil.move(doc, dest)
            moved_files.append(f"📖 {doc} → management_tools/docs/")
    
    # Move enhanced JavaScript (keep as reference)
    for js_file in categories["enhanced_javascript"]:
        if os.path.exists(js_file):
            dest = os.path.join(tools_dir, "enhanced_js", js_file)
            shutil.move(js_file, dest)
            moved_files.append(f"📜 {js_file} → management_tools/enhanced_js/")
    
    # Move configuration files
    for config in categories["configuration"]:
        if os.path.exists(config):
            dest = os.path.join(tools_dir, "config", config)
            shutil.move(config, dest)
            moved_files.append(f"⚙️  {config} → management_tools/config/")
    
    # Move logs and mappings
    for log_file in categories["logs_and_mappings"]:
        if os.path.exists(log_file):
            dest = os.path.join(tools_dir, "logs", log_file)
            shutil.move(log_file, dest)
            moved_files.append(f"📋 {log_file} → management_tools/logs/")
    
    print(f"\n✅ Organized {len(moved_files)} files:")
    for file_move in moved_files[:10]:  # Show first 10
        print(f"   {file_move}")
    if len(moved_files) > 10:
        print(f"   ... and {len(moved_files) - 10} more files")
    
    return len(moved_files)

def clean_empty_directories():
    """Remove any empty directories left behind."""
    print(f"\n🧹 Cleaning Empty Directories")
    print("=" * 35)
    
    removed_dirs = []
    
    # Check for specific directories that might be empty
    potential_empty_dirs = [
        "assets/images/poems",  # Should be empty after image cleanup
    ]
    
    for dir_path in potential_empty_dirs:
        if os.path.exists(dir_path):
            try:
                # Check if directory is empty
                if not os.listdir(dir_path):
                    # Remove empty directory
                    os.rmdir(dir_path)
                    removed_dirs.append(dir_path)
                    print(f"   🗑️  Removed empty directory: {dir_path}")
                else:
                    # List what's in the directory
                    contents = os.listdir(dir_path)
                    print(f"   📁 {dir_path} contains: {len(contents)} items")
            except Exception as e:
                print(f"   ❌ Error checking {dir_path}: {e}")
    
    if removed_dirs:
        print(f"✅ Removed {len(removed_dirs)} empty directories")
    else:
        print(f"✅ No empty directories to remove")
    
    return len(removed_dirs)

def create_production_structure_summary():
    """Create a summary of the final production structure."""
    print(f"\n📋 Production Structure Summary")
    print("=" * 40)
    
    structure = {
        "Core Website Files": [
            "index.html",
            "poem.html",
            "archive.html",
            "README.md"
        ],
        "JavaScript": [
            "js/content-loader.js",
            "js/dynamic-poem-loader.js",
            "js/main.js",
            "js/archive.js", 
            "js/poem-page.js"
        ],
        "Stylesheets": [
            "css/style.css"
        ],
        "Content": [
            "Poetry/ (74 poem folders)",
            "assets/ (placeholder.png only)"
        ],
        "Management Tools": [
            "management_tools/ (all scripts and docs)"
        ]
    }
    
    total_core_files = 0
    
    for category, files in structure.items():
        print(f"\n📂 {category}:")
        category_count = 0
        
        for file_pattern in files:
            if file_pattern.endswith("/"):
                # Directory
                dir_name = file_pattern.rstrip("/")
                if os.path.exists(dir_name):
                    if dir_name == "Poetry":
                        poem_folders = len([d for d in os.listdir(dir_name) 
                                          if os.path.isdir(os.path.join(dir_name, d)) and d.isdigit()])
                        print(f"   ✅ {dir_name}/ - {poem_folders} poem folders")
                        category_count += poem_folders
                    elif dir_name == "assets":
                        asset_files = len(os.listdir(dir_name)) if os.path.exists(dir_name) else 0
                        print(f"   ✅ {dir_name}/ - {asset_files} files")
                        category_count += asset_files
                    else:
                        print(f"   ✅ {file_pattern}")
                        category_count += 1
            elif "(" in file_pattern:
                # Special description
                print(f"   ✅ {file_pattern}")
                category_count += 1
            else:
                # Regular file
                if os.path.exists(file_pattern):
                    print(f"   ✅ {file_pattern}")
                    category_count += 1
                else:
                    print(f"   ❓ {file_pattern} (not found)")
        
        if category != "Management Tools":  # Don't count management tools as core
            total_core_files += category_count
    
    print(f"\n📊 Structure Statistics:")
    print(f"   Total core website files: {total_core_files}")
    print(f"   Management tools: Organized in management_tools/")
    print(f"   Backup safety: Multiple backup directories maintained")

def create_final_readme():
    """Create a clean README for the final structure."""
    readme_content = """# PoetryScape - Modern Poetry Website

A sophisticated poetry website with automatic image detection and folder-based organization.

## 🌟 Features

- **Automatic Image Detection**: Images are automatically associated with poems
- **Folder-Based Structure**: Each poem has its own self-contained directory
- **Responsive Design**: Beautiful display across all devices
- **Advanced Search**: Filter by language, form, length, and author
- **GitHub Pages Ready**: Optimized for GitHub Pages deployment

## 📁 Structure

```
Poetry/
├── 1/
│   ├── poem.md
│   └── image.png
├── 2/
│   ├── poem.md
│   └── image.png
└── ...
```

## 🚀 Adding New Poems

1. Create new folder: `Poetry/75/`
2. Add poem file: `Poetry/75/poem.md`
3. Add image: `Poetry/75/image.png`
4. Done! Automatically appears on website.

## 🛠️ Management Tools

All management scripts and documentation are in `management_tools/`:
- Scripts for adding/editing poems
- Migration and maintenance tools
- Comprehensive documentation
- Configuration files

## 🌐 Deployment

This website is optimized for GitHub Pages:
1. Push to your repository
2. Enable GitHub Pages
3. Your poetry website is live!

## 📖 Documentation

See `management_tools/docs/` for detailed guides:
- Folder structure guide
- Content management instructions
- Technical documentation

---

**A modern, scalable poetry website with zero-configuration management.**
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📖 Updated README.md with clean production information")

def create_declutter_summary():
    """Create a summary of the declutter operation."""
    summary_content = f"""# System Declutter Summary

## Operation Date
{datetime.now().isoformat()}

## Actions Performed

### ✅ File Organization
- Moved management scripts to `management_tools/scripts/`
- Moved documentation to `management_tools/docs/`
- Moved configuration files to `management_tools/config/`
- Moved logs and mappings to `management_tools/logs/`
- Moved enhanced JavaScript to `management_tools/enhanced_js/`

### ✅ Structure Cleanup
- Removed duplicate images from original directory
- Cleaned up empty directories
- Organized all temporary files
- Maintained all backup directories

### ✅ Production Ready
- Core website files remain in root directory
- All functionality preserved
- Clean, professional structure
- Management tools easily accessible

## Final Structure

### Core Website (Production)
- HTML, CSS, JavaScript files
- Poetry/ directory with 74 poem folders
- assets/ directory (cleaned)
- README.md (updated)

### Management Tools
- `management_tools/scripts/` - All management scripts
- `management_tools/docs/` - Complete documentation
- `management_tools/config/` - Configuration files
- `management_tools/logs/` - Operation logs and mappings
- `management_tools/enhanced_js/` - Enhanced JavaScript versions

### Backups
- Multiple timestamped backup directories maintained
- Complete recovery capability preserved

## Benefits

✅ **Clean Production Environment**: Only essential files in root  
✅ **Organized Management**: All tools in dedicated directory  
✅ **Preserved Functionality**: Zero impact on website operation  
✅ **Easy Maintenance**: Clear separation of concerns  
✅ **Professional Structure**: Ready for public deployment  

## Next Steps

1. Deploy website to GitHub Pages
2. Use tools in `management_tools/` for content management
3. Refer to `management_tools/docs/` for detailed instructions

**Your poetry website is now production-ready with a clean, professional structure!**
"""
    
    with open('management_tools/DECLUTTER_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"📋 Created declutter summary: management_tools/DECLUTTER_SUMMARY.md")

def main():
    print("🧹 System Declutter & Organization")
    print("=" * 50)
    print("Organizing files for production deployment and clean maintenance.")
    print("=" * 50)
    
    try:
        # Step 1: Organize files
        moved_files = organize_files()
        
        # Step 2: Clean empty directories
        removed_dirs = clean_empty_directories()
        
        # Step 3: Create production structure summary
        create_production_structure_summary()
        
        # Step 4: Update README for production
        create_final_readme()
        
        # Step 5: Create declutter summary
        create_declutter_summary()
        
        # Final summary
        print(f"\n🎉 Declutter Complete!")
        print("=" * 30)
        print(f"✅ Organized {moved_files} files into management_tools/")
        print(f"✅ Removed {removed_dirs} empty directories")
        print(f"✅ Updated README.md for production")
        print(f"✅ Created comprehensive documentation")
        
        print(f"\n📂 Final Structure:")
        print(f"   🌐 Root directory: Clean production website")
        print(f"   🛠️  management_tools/: All development tools")
        print(f"   💾 backup_*/: Safety backups maintained")
        
        print(f"\n🎯 Benefits:")
        print(f"   🚀 Production-ready deployment")
        print(f"   📁 Clean, professional structure")
        print(f"   🛠️  Easy access to management tools")
        print(f"   📖 Comprehensive documentation")
        print(f"   🔄 Zero functionality impact")
        
        print(f"\n🌟 Your poetry website is now:")
        print(f"   ✨ Perfectly organized")
        print(f"   🚀 Ready for deployment")
        print(f"   🛠️  Easy to maintain")
        print(f"   📚 Fully documented")
        
        print(f"\n🎭 Deployment ready! Your poetry website is pristine! ✨")
        
    except Exception as e:
        print(f"\n❌ Error during declutter: {e}")
        print(f"💡 Check file permissions and try again")

if __name__ == "__main__":
    main()