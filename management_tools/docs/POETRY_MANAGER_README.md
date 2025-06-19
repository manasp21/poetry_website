# Poetry Management System

A comprehensive Python tool for managing poetry content with ID-based linking, safe migration capabilities, and advanced management features.

## 🌟 Key Features

### 🚀 ID-Based System Migration
- **Safe Migration**: Convert from title-based to ID-based naming (poem001.md, image001.png)
- **Complete Backup**: Automatic backups before any changes
- **Rollback Capability**: Restore previous state if needed
- **Consistency Checks**: Validate all operations maintain website functionality

### 🖼️ Advanced Image Management
- **Manual Assignment**: Interactive interface to assign images to poems
- **Auto-Suggestions**: AI-powered image assignment suggestions
- **Orphan Detection**: Find unlinked images and poems without images
- **Bulk Operations**: Process multiple assignments at once

### 🔍 Validation & Testing
- **Registry Integrity**: Comprehensive validation of all data
- **Website Functionality**: Test that website works after changes
- **Missing File Detection**: Find broken links and missing resources
- **Metadata Validation**: Ensure all required fields are present

### 📊 Analytics & Reporting
- **Collection Statistics**: Detailed breakdowns by language, form, length
- **Image Coverage Reports**: Track assignment rates and gaps
- **Full System Reports**: Comprehensive health checks

## 📁 Current Structure Analysis

Based on your current poetry collection:

- **74 poems** across multiple categories
- **79 images** in the assets directory
- **28 poems** currently without assigned images
- **35 orphaned images** not linked to any poem

### Directory Structure
```
Poetry/
├── by_language/
│   ├── english/
│   │   ├── lengths/short/ (44 poems)
│   │   ├── forms/free_verse/ (26 poems)
│   │   └── forms/sonnet/ (1 poem)
│   └── hindi/
│       └── lengths/standard/ (1 poem)
└── [After migration: poem001.md, poem002.md, ...]

assets/images/poems/
├── [Current: title-based names]
└── [After migration: image001.png, image002.png, ...]
```

## 🚀 Quick Start Guide

### 1. Initial Setup & Analysis
```bash
# Test current structure
python3 test_poetry_manager.py

# Launch main interface
python3 poetry_manager.py
```

### 2. Generate Registry (First Time)
1. Choose **"Migration Operations"**
2. Select **"Generate Registry from Current Files"**
3. This creates `poem_registry.json` with all your content mapped

### 3. Migration Process (Optional but Recommended)
1. Choose **"Perform Full Migration to ID-Based System"**
2. Type `I UNDERSTAND` to confirm
3. Type `MIGRATE` for final confirmation
4. System will:
   - Create complete backup
   - Rename all files to ID-based names
   - Update all references
   - Update JavaScript files
   - Validate everything works

## 🎯 Main Menu Options

### 🚀 Migration Operations
- **Analyze Current Structure**: Review existing poems and images
- **Generate Registry**: Create central registry from current files
- **Perform Full Migration**: Convert to ID-based system
- **Rollback Migration**: Restore from backup if needed
- **Update JavaScript Files**: Sync with content-loader.js

### 🖼️ Image Management
- **List Unassigned Images**: See images not linked to poems
- **List Poems Without Images**: Find poems needing images
- **Manual Image Assignment**: Interactive assignment interface
- **Auto-Suggest Assignments**: AI-powered matching suggestions

### 🔍 Validation & Testing
- **Validate Registry Integrity**: Check for data consistency
- **Test Website Functionality**: Ensure site works correctly
- **Generate Full Report**: Comprehensive system health check

### 📦 Bulk Operations
- **Collection Statistics**: Detailed analytics
- **Bulk Metadata Update**: Update multiple poems at once
- **Regenerate All IDs**: Restructure ID assignments

## 💾 Registry System

The `poem_registry.json` file serves as the central database:

```json
{
  "poems": {
    "poem001": {
      "title": "A Leaf in a Sea of Green",
      "author": "Manas Pandey",
      "language": "en",
      "form": "short",
      "length": "short",
      "image_id": "image001",
      "content": "...",
      "original_filename": "a-leaf-in-a-sea-of-green_...",
      "created_date": "2024-01-01",
      "last_modified": "2024-01-01"
    }
  },
  "images": {
    "image001": {
      "original_filename": "a-leaf-in-a-sea-of-green.png",
      "linked_poem": "poem001"
    }
  }
}
```

## 🛡️ Safety Features

### Automatic Backups
- Created before any major operation
- Timestamped for easy identification
- Include all poems, images, and JavaScript files

### Validation Checks
- **Pre-migration**: Analyze current structure
- **During migration**: Verify each step
- **Post-migration**: Test website functionality
- **Rollback**: Restore if issues detected

### Consistency Guarantees
- All poem-image links preserved
- Metadata integrity maintained
- Website functionality unchanged
- GitHub Pages compatibility ensured

## 🔧 Advanced Usage

### Manual Image Assignment Example
```
📝 Poem: poem023
   Title: Jupiter Shone Different
   Author: Manas Pandey
   Preview: In a sky filled with
             stars that dance like
             whispered secrets...

🖼️ Available images:
   1. image050 (was: jupiter-shone-different.png)
   2. image051 (was: sirius-in-the-sky.png)
   3. image052 (was: magnificent-arent-they.png)

Assign image to 'Jupiter Shone Different'? (number/skip/quit): 1
✅ Assigned image050 to poem023
```

### Auto-Suggestion Example
```
🤖 Auto-suggestions (15 found):
   • poem023 (Jupiter Shone Different) → image050 (was: jupiter-shone-different.png)
   • poem041 (Sirius in the Sky) → image051 (was: sirius-in-the-sky.png)
   • poem007 (Cold Hallways) → image052 (was: cold-hallways.png)
```

## 🌐 Website Integration

### JavaScript Updates
The system automatically updates:
- `js/content-loader.js`: Static poem paths array
- `js/dynamic-poem-loader.js`: Fallback paths

### Path Compatibility
- Maintains `/poetry_website/` prefix for GitHub Pages
- Preserves all existing functionality
- No changes to user experience

## 📊 Expected Benefits

### After Migration:
1. **Simplified Management**: Easy to reference poems by ID
2. **Bulk Operations**: Process multiple poems efficiently
3. **Better Organization**: Clear ID-based structure
4. **Enhanced Features**: Image assignment, validation, reporting
5. **Future-Proof**: Extensible system for new features

### Performance:
- Faster poem loading (shorter paths)
- Improved caching (predictable names)
- Better error handling (ID validation)

## 🚨 Important Notes

### Before Migration:
- ✅ Test script runs successfully
- ✅ All poems and images are accounted for
- ✅ Website functions correctly locally
- ✅ Backup system works

### After Migration:
- ✅ All poems load correctly
- ✅ All images display properly
- ✅ Search and filtering work
- ✅ GitHub Pages deployment succeeds

## 🆘 Troubleshooting

### Common Issues:

**"Registry validation failed"**
- Run validation checks to identify specific issues
- Use the full report for detailed diagnostics

**"Migration failed"**
- Check error messages for specific problems
- Use rollback to restore previous state
- Review backup directory for manual recovery

**"Images not displaying"**
- Verify image files exist in correct location
- Check poem registry for correct image_id references
- Run image validation tools

**"Website broken after migration"**
- Use rollback immediately: Migration Menu → Rollback Migration
- Check JavaScript files were updated correctly
- Verify all paths use proper GitHub Pages prefix

### Getting Help:
1. Run `python3 test_poetry_manager.py` for quick diagnostics
2. Use "Generate Full Report" for comprehensive analysis
3. Check backup directories for manual recovery options

## 🔮 Future Enhancements

Planned features:
- Web interface for remote management
- Integration with GitHub API for automatic deployment
- Advanced search and tagging system
- Content versioning and history
- Multi-language support expansion
- Automated content generation tools

---

**Created for PoetryScape website management**  
**Safe, reliable, and feature-rich poetry content management**