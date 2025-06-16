# Simple Poem Management Guide

## 🎯 Easy File-Based Poem Management

This guide shows you the simple way to add, edit, and manage poems on your PoetryScape website by working directly with files.

## 🚀 Quick Start (No Setup Required!)

Your website now automatically discovers new poems - just add files and they appear on the site!

## 📝 Three Ways to Add Poems

### Method 1: Use the Simple Python Script (Easiest)

1. **Run the poem creator**:
   ```bash
   python create-poem.py
   ```

2. **Follow the prompts**:
   - Enter poem title
   - Choose category (short, free verse, sonnet, Hindi)
   - Type your poem content
   - Optionally specify an image filename

3. **Done!** The script creates the file in the right place automatically.

### Method 2: Create Files Manually

1. **Choose the right directory**:
   - Short poems: `Poetry/by_language/english/lengths/short/`
   - Free verse: `Poetry/by_language/english/forms/free_verse/`
   - Sonnets: `Poetry/by_language/english/forms/sonnet/`
   - Hindi poems: `Poetry/by_language/hindi/lengths/standard/`

2. **Create a new `.md` file** with this format:
   ```markdown
   ---
   title: "Your Poem Title"
   author: "Manas Pandey"
   original_path: "Poetry/..."
   language: "en"
   form: "short"
   length: "short"
   image: "your-image.png"
   ---
   Your poem content goes here.
   
   Multiple stanzas work fine.
   Just separate them with blank lines.
   ```

3. **Save the file** with a descriptive name ending in `.md`

### Method 3: Copy and Modify Existing Poem

1. **Copy an existing poem file** that's similar to what you want
2. **Edit the content** - change title, content, image, etc.
3. **Save with a new filename**

## 🖼️ Adding Images

1. **Add your image** to `assets/images/poems/`
2. **Use .png or .jpg format**
3. **Name it something descriptive** (e.g., `sunset-memories.png`)
4. **Reference it in your poem** with `image: "sunset-memories.png"`

## ✏️ Editing Existing Poems

### Quick Edit with Management Script:
```bash
python manage-poems.py
```
This will show you all poems and let you:
- List all poems
- Edit any poem (opens in your default editor)
- Delete poems safely
- Check which poems have images

### Manual Edit:
1. **Find the poem file** in the appropriate directory
2. **Open it in any text editor**
3. **Make your changes**
4. **Save the file**

## 🛠️ How It Works

### Automatic Discovery
Your website now **automatically finds new poems**! Here's how:

1. **Add any .md file** to the poem directories
2. **Commit and push** to GitHub
3. **Wait 2-3 minutes** for GitHub Pages to rebuild
4. **Your poem appears automatically** on the website!

### Directory Structure
```
Poetry/
├── by_language/
│   ├── english/
│   │   ├── lengths/short/     # Short poems
│   │   └── forms/
│   │       ├── free_verse/    # Free verse poems
│   │       └── sonnet/        # Sonnets
│   └── hindi/
│       └── lengths/standard/  # Hindi poems
```

### What Happens Automatically
1. **Discovery**: Website scans directories for .md files
2. **Loading**: Reads YAML frontmatter and content
3. **Display**: Shows poems on homepage and archive
4. **Images**: Links images automatically if specified
5. **No manual updates needed** - everything just works!

## 🔧 Troubleshooting

### Poems Not Appearing
- **Wait 2-3 minutes** for GitHub Pages to rebuild after pushing
- Check that your file is in the correct directory
- Verify the YAML frontmatter is properly formatted
- Make sure the file ends with `.md`

### Python Scripts Not Working
- Make sure you have Python installed (`python --version`)
- Run from the repository root directory
- Check that you have write permissions

### Images Not Showing
- Verify image is in `assets/images/poems/` directory
- Check the filename matches exactly (case-sensitive)
- Ensure image format is PNG or JPG
- Verify the `image:` field in your poem frontmatter

### File Format Issues
- Use UTF-8 encoding for all text files
- Make sure YAML frontmatter starts and ends with `---`
- Don't use tabs in YAML, only spaces
- Put quotes around titles and author names

## 🚀 Simple Publishing Workflow

### Your Easy Process:
1. **Create poem** (using script or manually)
2. **Add image** (optional) to `assets/images/poems/`
3. **Commit and push** to GitHub
4. **Wait 2-3 minutes** for automatic deployment
5. **Enjoy!** Your poem is live on the website

### For Managing Existing Poems:
1. **Run** `python manage-poems.py`
2. **Choose option** (list, edit, delete, check images)
3. **Make changes** as needed
4. **Commit and push** to see changes live

## 🎉 Success! Simple Poem Management is Ready

You now have a simple, reliable poem management system:

✅ **No complex setup** - just add files and they appear  
✅ **Automatic discovery** - website finds new poems automatically  
✅ **Simple tools** - Python scripts for easy poem creation  
✅ **Direct file editing** - use any text editor you like  
✅ **Image support** - just drop images in the folder  
✅ **Instant publishing** - push to GitHub and it's live  
✅ **No authentication issues** - just file management  

**Perfect for:**
- Adding poems quickly from your computer
- Editing poems in your favorite text editor
- Simple workflow without web interfaces
- Full control over your content files

**Next Steps:**
1. Try `python create-poem.py` to add your first poem
2. Use `python manage-poems.py` to explore existing poems
3. Add some images to `assets/images/poems/`
4. Commit and push to see everything live!