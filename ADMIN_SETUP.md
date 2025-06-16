# PoetryScape Admin Setup Guide

## 🎯 Complete Poem Management System

This guide will help you set up the admin interface to add, edit, and delete poems on your PoetryScape website.

## 🔐 Authentication Setup

### Step 1: Enable Netlify Identity (Recommended)

1. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository (`manasp21/poetry_website`)
   - Deploy the site

2. **Enable Netlify Identity**:
   - In Netlify dashboard → Site settings → Identity
   - Click "Enable Identity"
   - Under "Registration preferences" → Select "Invite only"
   - Under "External providers" → Add "GitHub" (recommended)

3. **Add Your Admin Account**:
   - Go to Identity tab in Netlify dashboard
   - Click "Invite users"
   - Add your email address
   - You'll receive an invitation email

4. **Configure Git Gateway**:
   - In Identity settings → Services → Git Gateway
   - Click "Enable Git Gateway"
   - This allows the CMS to commit directly to GitHub

### Step 2: Alternative GitHub Authentication

If you prefer direct GitHub authentication:

1. **Create GitHub OAuth App**:
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Click "New OAuth App"
   - Application name: "PoetryScape Admin"
   - Homepage URL: `https://manasp21.github.io/poetry_website`
   - Authorization callback URL: `https://api.netlify.com/auth/done`

2. **Update Config**:
   - Copy Client ID and Client Secret
   - Add to your Netlify site's environment variables

## 📝 Using the Admin Interface

### Accessing Admin Panel

1. **Visit Admin URL**:
   ```
   https://manasp21.github.io/poetry_website/admin/
   ```

2. **Login**:
   - Use your GitHub account or Netlify Identity
   - Only authorized users can access

### Adding New Poems

1. **Choose Collection**:
   - **Short Poems**: Brief poems, haikus, etc.
   - **Free Verse Poems**: Longer poems without strict form
   - **Sonnets**: Traditional 14-line poems
   - **Hindi Poems**: Poems in Hindi language

2. **Fill Required Fields**:
   ```yaml
   Title: "Your Poem Title"           # Required
   Author: "Manas Pandey"            # Pre-filled
   Language: en/hi                    # Auto-selected
   Form: short/free_verse/sonnet     # Based on collection
   Featured Image: [Upload or skip]   # Optional
   Poem Content: [Write your poem]    # Required
   ```

3. **Preview & Publish**:
   - Use the preview tab to see how it will look
   - Click "Publish" to save to GitHub
   - Poem appears on website within minutes

### Editing Existing Poems

1. **Browse Collections**:
   - Click on any collection in admin panel
   - See list of all poems in that category

2. **Edit Content**:
   - Click on any poem to edit
   - Modify title, content, image, or metadata
   - Changes save directly to GitHub

3. **Live Preview**:
   - Use preview tab while editing
   - See real-time formatting

### Deleting Poems

1. **Select Poem**:
   - Go to collection → Select poem

2. **Delete Safely**:
   - Click delete button
   - Confirm deletion in dialog
   - File removed from GitHub automatically

## 🛠️ How It Works

### File Organization

The admin automatically organizes poems into the correct directories:

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

### Automatic Features

1. **File Naming**: Generates proper filenames automatically
2. **Image Upload**: Handles image upload to `/assets/images/poems/`
3. **Metadata**: Auto-fills required YAML frontmatter
4. **Discovery**: New poems appear on website automatically
5. **Validation**: Prevents invalid content submission

### Dynamic Content Loading

- Website automatically discovers new poems
- No manual file updates needed
- Uses GitHub API for dynamic discovery
- Fallback to static list if API unavailable

## 🔧 Troubleshooting

### Admin Won't Load
- Check internet connection
- Verify GitHub repository permissions
- Clear browser cache

### Can't Login
- Ensure you're invited to Netlify Identity
- Try GitHub authentication
- Check repository access permissions

### Poems Not Appearing
- Wait 2-3 minutes for GitHub Pages rebuild
- Check admin for successful publication
- Verify file was created in correct directory

### Image Upload Issues
- Use PNG/JPG formats
- Keep images under 2MB
- Check file naming (no special characters)

## 📊 Admin Dashboard Features

### Content Overview
- Total poems by category
- Recent additions
- Quick edit links

### Rich Text Editor
- Markdown support
- Live preview
- Syntax highlighting

### Image Management
- Drag-and-drop upload
- Automatic optimization
- Gallery view

### Search & Filter
- Find poems quickly
- Filter by category
- Sort by date/title

## 🚀 Publishing Workflow

### Immediate Publishing
1. Write poem in admin
2. Click "Publish"
3. Auto-commit to GitHub
4. Site rebuilds automatically
5. Live within 2-3 minutes

### Draft Workflow (Optional)
1. Save as draft
2. Review and edit
3. Publish when ready
4. Perfect for multiple revisions

## 📱 Mobile Access

The admin interface is fully responsive:
- Add poems from phone/tablet
- Edit content on the go
- Upload images from camera
- Full functionality on mobile

## 🎉 Success! Your Admin System is Ready

You now have a complete content management system for your poetry website:

✅ **Easy poem addition** via web interface  
✅ **Edit any existing poem** with rich editor  
✅ **Delete poems safely** with confirmation  
✅ **Secure access** - only you can manage content  
✅ **Mobile-friendly** - manage from anywhere  
✅ **Automatic organization** - no technical knowledge needed  
✅ **Live preview** - see exactly how poems will look  
✅ **Image upload** - add visual elements easily  

**Next Steps**:
1. Set up authentication (Netlify Identity recommended)
2. Access admin panel and add your first poem
3. Explore the different poem collections
4. Enjoy effortless poem management!

For support or questions, refer to the Netlify CMS documentation or GitHub repository issues.