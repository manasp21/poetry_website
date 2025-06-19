# Poetry Management CLI - User Guide

## 🎭 Overview

A comprehensive command-line interface for managing your poetry collection with full CRUD operations, metadata management, and backup features.

## 🚀 Getting Started

### Running the CLI
```bash
python3 poetry_cli.py
```

### Testing the Installation
```bash
python3 test_poetry_cli.py
```

## 📝 Main Features

### 1. Poem Management
- **Add New Poems**: Create poems with full metadata (title, author, language, form, length)
- **Edit Existing Poems**: Modify content and metadata of any poem
- **Delete Poems**: Safe deletion with automatic backup
- **View Poems**: Display poem details including metadata
- **List Poems**: Browse all poems with optional filtering
- **Search Poems**: Find poems by title or content

### 2. Metadata Management
- **View Categories**: See all available forms, lengths, and languages
- **Add New Forms**: Dynamically add new poetry forms (e.g., "Haiku", "Limerick")
- **Add New Lengths**: Add new length categories (e.g., "Epic", "Micro")
- **Add New Languages**: Support for multiple languages with codes
- **Remove Categories**: Clean up unused metadata

### 3. Advanced Image Management
- **Direct Assignment**: Add images directly to poems from file system
- **Image Store**: Central repository for managing images before assignment
- **Bulk Import**: Import entire directories of images at once
- **Browse & Search**: View all stored images with details (size, format, date)
- **Flexible Assignment**: Assign stored images to any poem
- **Multiple Formats**: Support for PNG, JPG, JPEG, WEBP, GIF, BMP formats
- **Smart Naming**: Automatic naming with timestamps and custom names
- **Image Details**: View file size, format, and modification dates

### 4. Tools & Validation
- **Collection Validation**: Check for missing files, invalid metadata
- **Backup System**: Create and restore backups
- **Repair Numbering**: Fix poem numbering to be sequential
- **Statistics**: View detailed collection statistics

## 🏷️ Current Metadata Options

### Poetry Forms
- Free Verse
- Sonnet  
- short

### Poetry Lengths
- Standard
- short

### Languages
- English (en)
- Hindi (hi)

## 📊 Current Collection Status

✅ **74 poems** successfully detected and validated
✅ **All poems** have properly formatted metadata
✅ **All poems** have assigned images
✅ **No validation issues** found

## 🔧 Advanced Features

### Automatic Backups
- Backups created before any destructive operation
- Restore from any backup with full collection state
- Backup manifest tracking

### Safety Features
- Confirmation prompts for deletion
- Automatic validation after operations
- Rollback capabilities

### Extensibility
- Easy addition of new metadata categories
- Support for bulk operations
- Comprehensive search and filtering

## 📖 Example Workflows

### Adding a New Poem
1. Choose "1. Manage Poems" → "1. Add New Poem"
2. Enter title, select metadata options
3. Input poem content (press Enter twice when done)
4. Optionally add an image

### Adding a New Poetry Form
1. Choose "2. Manage Metadata" → "2. Add New Form"
2. Enter the new form name (e.g., "Haiku")
3. Form is now available for all poems

### Managing Images Efficiently
1. **Bulk Import**: Choose "3. Manage Images" → "5. Bulk Add Images to Store"
   - Point to a directory containing your images
   - All supported formats are automatically imported
2. **Browse & Assign**: Choose "4. Browse Image Store"
   - View all available images with details
   - Select images and assign to specific poems
3. **Direct Assignment**: Choose "1. Add Image to Poem" for immediate assignment

### Image Store Workflow
1. **Build Library**: Add images to store from various sources
2. **Organize**: View images with sizes, dates, formats
3. **Assign**: Connect stored images to poems as needed
4. **Manage**: Remove unused images from store

### Bulk Operations
1. Use "5. Statistics" to analyze your collection
2. Use "4. Tools & Validation" for maintenance
3. Create regular backups for safety

## 🛠️ File Structure

```
Poetry/
├── 1/
│   ├── poem.md    # YAML frontmatter + content
│   └── image.png  # Associated image
├── 2/
│   ├── poem.md
│   └── image.png
└── ...

image_store/            # Central image repository
├── sunset_beach.png
├── mountain_view.jpg
├── abstract_art.webp
└── ...

poetry_metadata.json   # Categories configuration
backups/               # Automatic backups
└── backup_YYYYMMDD_HHMMSS/

test_image_features.py # Image testing script
```

## 🔍 Troubleshooting

### If poems aren't detected:
- Ensure poems are in `Poetry/X/poem.md` format
- Check YAML frontmatter is properly formatted
- Run collection validation

### If metadata is missing:
- Use "Tools & Validation" → "Validate Collection"
- Edit poems to add missing metadata
- Categories are automatically detected from existing poems

## 📚 Tips

1. **Regular Backups**: Create backups before major changes
2. **Consistent Metadata**: Use the predefined categories for consistency
3. **Sequential Numbering**: Use "Repair Numbering" if poem numbers get out of order
4. **Batch Operations**: Use filtering and search for bulk operations
5. **Image Store Strategy**: 
   - Build your image library first using bulk import
   - Use descriptive names when adding to store
   - Browse store before assignments to see available options
6. **Supported Image Formats**: PNG, JPG, JPEG, WEBP, GIF, BMP
7. **Image Organization**: Store keeps originals safe while converting for poems
8. **File Management**: Images are automatically converted to PNG for consistency

---

**Happy writing! 🎭✨**