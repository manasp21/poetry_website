#!/usr/bin/env python3
"""
Comprehensive Poetry Management CLI
==================================

A complete command-line interface for managing poetry with full CRUD operations,
metadata management, and safe backup features.

Features:
- Add new poems with full metadata
- Edit existing poems and metadata
- Delete poems safely with backup
- Manage poetry categories (forms, lengths, languages)
- Image handling and assignment
- Validation and consistency checks
- Backup and rollback capabilities

Author: Claude Code Assistant
"""

import os
import json
import yaml
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import glob


class MetadataManager:
    """Manages poetry metadata categories and options."""
    
    def __init__(self, config_file: str = "poetry_metadata.json"):
        self.config_file = config_file
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata configuration or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Default metadata based on current poems
        return {
            "forms": ["Free Verse", "Sonnet", "short"],
            "lengths": ["Standard", "short"],
            "languages": [
                {"code": "en", "name": "English"},
                {"code": "hi", "name": "Hindi"}
            ],
            "default_author": "Manas Pandey",
            "version": "1.0",
            "last_updated": datetime.now().isoformat()
        }
    
    def save_metadata(self) -> bool:
        """Save metadata configuration."""
        try:
            self.metadata["last_updated"] = datetime.now().isoformat()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving metadata: {e}")
            return False
    
    def get_forms(self) -> List[str]:
        """Get available poetry forms."""
        return self.metadata.get("forms", [])
    
    def get_lengths(self) -> List[str]:
        """Get available poetry lengths."""
        return self.metadata.get("lengths", [])
    
    def get_languages(self) -> List[Dict[str, str]]:
        """Get available languages."""
        return self.metadata.get("languages", [])
    
    def get_language_codes(self) -> List[str]:
        """Get language codes only."""
        return [lang["code"] for lang in self.get_languages()]
    
    def add_form(self, form: str) -> bool:
        """Add new poetry form."""
        if form in self.metadata["forms"]:
            print(f"⚠️  Form '{form}' already exists")
            return False
        
        self.metadata["forms"].append(form)
        self.save_metadata()
        print(f"✅ Added new form: {form}")
        return True
    
    def add_length(self, length: str) -> bool:
        """Add new poetry length."""
        if length in self.metadata["lengths"]:
            print(f"⚠️  Length '{length}' already exists")
            return False
        
        self.metadata["lengths"].append(length)
        self.save_metadata()
        print(f"✅ Added new length: {length}")
        return True
    
    def add_language(self, code: str, name: str) -> bool:
        """Add new language."""
        if any(lang["code"] == code for lang in self.metadata["languages"]):
            print(f"⚠️  Language code '{code}' already exists")
            return False
        
        self.metadata["languages"].append({"code": code, "name": name})
        self.save_metadata()
        print(f"✅ Added new language: {name} ({code})")
        return True
    
    def remove_form(self, form: str) -> bool:
        """Remove poetry form."""
        if form not in self.metadata["forms"]:
            print(f"❌ Form '{form}' not found")
            return False
        
        self.metadata["forms"].remove(form)
        self.save_metadata()
        print(f"✅ Removed form: {form}")
        return True
    
    def remove_length(self, length: str) -> bool:
        """Remove poetry length."""
        if length not in self.metadata["lengths"]:
            print(f"❌ Length '{length}' not found")
            return False
        
        self.metadata["lengths"].remove(length)
        self.save_metadata()
        print(f"✅ Removed length: {length}")
        return True
    
    def get_default_author(self) -> str:
        """Get default author name."""
        return self.metadata.get("default_author", "Unknown Author")


class BackupManager:
    """Handles backup and restore operations."""
    
    def __init__(self):
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, description: str = "Manual backup") -> str:
        """Create a backup of the Poetry directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup Poetry directory
            if os.path.exists("Poetry"):
                shutil.copytree("Poetry", os.path.join(backup_path, "Poetry"))
            
            # Create backup manifest
            manifest = {
                "timestamp": timestamp,
                "description": description,
                "poems_count": len(glob.glob("Poetry/*/poem.md")),
                "created_by": "poetry_cli"
            }
            
            with open(os.path.join(backup_path, "manifest.json"), 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✅ Backup created: {backup_name}")
            return backup_name
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return ""
    
    def list_backups(self) -> List[Dict[str, str]]:
        """List available backups."""
        backups = []
        if not os.path.exists(self.backup_dir):
            return backups
        
        for backup_name in os.listdir(self.backup_dir):
            backup_path = os.path.join(self.backup_dir, backup_name)
            manifest_path = os.path.join(backup_path, "manifest.json")
            
            if os.path.isdir(backup_path) and os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    manifest["name"] = backup_name
                    backups.append(manifest)
                except:
                    pass
        
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from backup."""
        backup_path = os.path.join(self.backup_dir, backup_name, "Poetry")
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        try:
            # Remove current Poetry directory
            if os.path.exists("Poetry"):
                shutil.rmtree("Poetry")
            
            # Restore from backup
            shutil.copytree(backup_path, "Poetry")
            print(f"✅ Restored from backup: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False


class PoemManager:
    """Manages CRUD operations for poems."""
    
    def __init__(self, metadata_manager: MetadataManager):
        self.metadata_manager = metadata_manager
        self.poetry_dir = "Poetry"
        os.makedirs(self.poetry_dir, exist_ok=True)
    
    def get_next_poem_number(self) -> int:
        """Get the next available poem number."""
        existing_numbers = []
        if os.path.exists(self.poetry_dir):
            for folder in os.listdir(self.poetry_dir):
                folder_path = os.path.join(self.poetry_dir, folder)
                if os.path.isdir(folder_path) and folder.isdigit():
                    existing_numbers.append(int(folder))
        
        return max(existing_numbers, default=0) + 1
    
    def create_poem(self, title: str, content: str, author: str = None, 
                   language: str = "en", form: str = "Free Verse", 
                   length: str = "Standard") -> Optional[int]:
        """Create a new poem."""
        if not title.strip() or not content.strip():
            print("❌ Title and content are required")
            return None
        
        poem_number = self.get_next_poem_number()
        poem_dir = os.path.join(self.poetry_dir, str(poem_number))
        
        try:
            # Create poem directory
            os.makedirs(poem_dir, exist_ok=True)
            
            # Prepare metadata
            if not author:
                author = self.metadata_manager.get_default_author()
            
            # Create poem content
            poem_data = {
                "title": title.strip(),
                "author": author.strip(),
                "language": language,
                "form": form,
                "length": length
            }
            
            poem_content = "---\n"
            for key, value in poem_data.items():
                poem_content += f'{key}: "{value}"\n'
            poem_content += "---\n" + content.strip()
            
            # Write poem file
            poem_file = os.path.join(poem_dir, "poem.md")
            with open(poem_file, 'w', encoding='utf-8') as f:
                f.write(poem_content)
            
            print(f"✅ Created poem #{poem_number}: {title}")
            
            # Automatically update JavaScript files for website
            self._update_javascript_paths()
            
            return poem_number
            
        except Exception as e:
            print(f"❌ Error creating poem: {e}")
            return None
    
    def _update_javascript_paths(self):
        """Update JavaScript files with current poem paths."""
        try:
            # Get all current poem paths
            poem_paths = []
            if os.path.exists(self.poetry_dir):
                for folder in sorted(os.listdir(self.poetry_dir), key=lambda x: int(x) if x.isdigit() else 0):
                    folder_path = os.path.join(self.poetry_dir, folder)
                    poem_file = os.path.join(folder_path, "poem.md")
                    
                    if os.path.isdir(folder_path) and folder.isdigit() and os.path.exists(poem_file):
                        poem_paths.append(f"Poetry/{folder}/poem.md")
            
            # Update JavaScript files
            js_files = [
                "js/content-loader.js",
                "js/dynamic-poem-loader.js"
            ]
            
            for js_file in js_files:
                if os.path.exists(js_file):
                    with open(js_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Create new paths array
                    paths_array = '[\n'
                    for path in poem_paths:
                        paths_array += f'        "{path}",\n'
                    paths_array = paths_array.rstrip(',\n') + '\n    ]'
                    
                    # Update the appropriate array
                    if "poemFilePaths" in content:
                        pattern = r'const poemFilePaths = \[[\s\S]*?\];'
                        new_content = re.sub(
                            pattern,
                            f'const poemFilePaths = {paths_array};',
                            content,
                            count=1
                        )
                    elif "staticPaths" in content:
                        pattern = r'const staticPaths = \[[\s\S]*?\];'
                        new_content = re.sub(
                            pattern,
                            f'const staticPaths = {paths_array};',
                            content,
                            count=1
                        )
                    else:
                        continue
                    
                    if new_content != content:
                        with open(js_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
            
            print(f"🌐 Updated website JavaScript files for {len(poem_paths)} poems")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not update JavaScript files: {e}")
    
    def get_poem(self, poem_number: int) -> Optional[Dict[str, Any]]:
        """Get poem data by number."""
        poem_dir = os.path.join(self.poetry_dir, str(poem_number))
        poem_file = os.path.join(poem_dir, "poem.md")
        
        if not os.path.exists(poem_file):
            return None
        
        try:
            with open(poem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            parts = content.split("---", 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1]) or {}
                poem_content = parts[2].strip()
            else:
                metadata = {}
                poem_content = content
            
            return {
                "number": poem_number,
                "metadata": metadata,
                "content": poem_content,
                "file_path": poem_file,
                "has_image": os.path.exists(os.path.join(poem_dir, "image.png"))
            }
            
        except Exception as e:
            print(f"❌ Error reading poem {poem_number}: {e}")
            return None
    
    def update_poem(self, poem_number: int, title: str = None, content: str = None,
                   author: str = None, language: str = None, form: str = None,
                   length: str = None) -> bool:
        """Update an existing poem."""
        poem_data = self.get_poem(poem_number)
        if not poem_data:
            print(f"❌ Poem #{poem_number} not found")
            return False
        
        try:
            # Update metadata
            metadata = poem_data["metadata"]
            if title is not None:
                metadata["title"] = title.strip()
            if author is not None:
                metadata["author"] = author.strip()
            if language is not None:
                metadata["language"] = language
            if form is not None:
                metadata["form"] = form
            if length is not None:
                metadata["length"] = length
            
            # Update content
            if content is not None:
                poem_content = content.strip()
            else:
                poem_content = poem_data["content"]
            
            # Write updated poem
            updated_content = "---\n"
            for key, value in metadata.items():
                updated_content += f'{key}: "{value}"\n'
            updated_content += "---\n" + poem_content
            
            with open(poem_data["file_path"], 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated poem #{poem_number}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating poem: {e}")
            return False
    
    def delete_poem(self, poem_number: int) -> bool:
        """Delete a poem (with backup)."""
        poem_dir = os.path.join(self.poetry_dir, str(poem_number))
        
        if not os.path.exists(poem_dir):
            print(f"❌ Poem #{poem_number} not found")
            return False
        
        try:
            # Get poem info for confirmation
            poem_data = self.get_poem(poem_number)
            if poem_data:
                title = poem_data["metadata"].get("title", f"Poem #{poem_number}")
                print(f"🗑️  Deleting poem #{poem_number}: {title}")
            
            # Remove directory
            shutil.rmtree(poem_dir)
            print(f"✅ Deleted poem #{poem_number}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting poem: {e}")
            return False
    
    def list_poems(self, filter_by: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """List all poems with optional filtering."""
        poems = []
        
        if not os.path.exists(self.poetry_dir):
            return poems
        
        for folder in sorted(os.listdir(self.poetry_dir), key=lambda x: int(x) if x.isdigit() else 0):
            if folder.isdigit():
                poem_data = self.get_poem(int(folder))
                if poem_data:
                    # Apply filters
                    if filter_by:
                        match = True
                        for key, value in filter_by.items():
                            if poem_data["metadata"].get(key, "").lower() != value.lower():
                                match = False
                                break
                        if not match:
                            continue
                    
                    poems.append(poem_data)
        
        return poems
    
    def search_poems(self, query: str) -> List[Dict[str, Any]]:
        """Search poems by title or content."""
        results = []
        query_lower = query.lower()
        
        for poem_data in self.list_poems():
            title = poem_data["metadata"].get("title", "").lower()
            content = poem_data["content"].lower()
            
            if query_lower in title or query_lower in content:
                results.append(poem_data)
        
        return results


class ImageManager:
    """Manages poem images."""
    
    def __init__(self):
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp']
        self.image_store_dir = "image_store"
        os.makedirs(self.image_store_dir, exist_ok=True)
    
    def add_image_to_poem(self, poem_number: int, image_path: str) -> bool:
        """Add an image to a poem."""
        poem_dir = os.path.join("Poetry", str(poem_number))
        
        if not os.path.exists(poem_dir):
            print(f"❌ Poem #{poem_number} not found")
            return False
        
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
        
        try:
            # Copy image to poem directory as image.png
            dest_path = os.path.join(poem_dir, "image.png")
            shutil.copy2(image_path, dest_path)
            print(f"✅ Added image to poem #{poem_number}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding image: {e}")
            return False
    
    def remove_image_from_poem(self, poem_number: int) -> bool:
        """Remove image from a poem."""
        poem_dir = os.path.join("Poetry", str(poem_number))
        image_path = os.path.join(poem_dir, "image.png")
        
        if not os.path.exists(image_path):
            print(f"❌ No image found for poem #{poem_number}")
            return False
        
        try:
            os.remove(image_path)
            print(f"✅ Removed image from poem #{poem_number}")
            return True
            
        except Exception as e:
            print(f"❌ Error removing image: {e}")
            return False
    
    def add_image_to_store(self, image_path: str, name: str = None) -> bool:
        """Add an image to the image store for later use."""
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
        
        # Get file extension
        _, ext = os.path.splitext(image_path)
        if ext.lower() not in self.image_extensions:
            print(f"❌ Unsupported image format: {ext}")
            print(f"Supported formats: {', '.join(self.image_extensions)}")
            return False
        
        try:
            # Generate name if not provided
            if not name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                original_name = os.path.splitext(os.path.basename(image_path))[0]
                name = f"{original_name}_{timestamp}"
            
            # Clean name for filename
            clean_name = re.sub(r'[^\w\s-]', '', name)
            clean_name = re.sub(r'\s+', '_', clean_name.strip())
            
            dest_path = os.path.join(self.image_store_dir, f"{clean_name}.png")
            
            # Check if file already exists
            counter = 1
            original_dest = dest_path
            while os.path.exists(dest_path):
                base_name = os.path.splitext(original_dest)[0]
                dest_path = f"{base_name}_{counter}.png"
                counter += 1
            
            shutil.copy2(image_path, dest_path)
            print(f"✅ Added image to store: {os.path.basename(dest_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding image to store: {e}")
            return False
    
    def list_store_images(self) -> List[Dict[str, Any]]:
        """List all images in the image store."""
        images = []
        
        if not os.path.exists(self.image_store_dir):
            return images
        
        for file in os.listdir(self.image_store_dir):
            file_path = os.path.join(self.image_store_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in self.image_extensions:
                    stat = os.stat(file_path)
                    images.append({
                        "name": file,
                        "path": file_path,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    })
        
        return sorted(images, key=lambda x: x["modified"], reverse=True)
    
    def assign_store_image_to_poem(self, poem_number: int, image_name: str) -> bool:
        """Assign an image from the store to a poem."""
        store_image_path = os.path.join(self.image_store_dir, image_name)
        
        if not os.path.exists(store_image_path):
            print(f"❌ Image not found in store: {image_name}")
            return False
        
        return self.add_image_to_poem(poem_number, store_image_path)
    
    def delete_store_image(self, image_name: str) -> bool:
        """Delete an image from the store."""
        store_image_path = os.path.join(self.image_store_dir, image_name)
        
        if not os.path.exists(store_image_path):
            print(f"❌ Image not found in store: {image_name}")
            return False
        
        try:
            os.remove(store_image_path)
            print(f"✅ Deleted image from store: {image_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting image: {e}")
            return False
    
    def bulk_add_images_to_store(self, directory_path: str) -> int:
        """Add all images from a directory to the store."""
        if not os.path.exists(directory_path):
            print(f"❌ Directory not found: {directory_path}")
            return 0
        
        added_count = 0
        
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in self.image_extensions:
                    base_name = os.path.splitext(file)[0]
                    if self.add_image_to_store(file_path, base_name):
                        added_count += 1
        
        print(f"✅ Added {added_count} images to store")
        return added_count
    
    def get_image_info(self, image_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an image in the store."""
        store_image_path = os.path.join(self.image_store_dir, image_name)
        
        if not os.path.exists(store_image_path):
            return None
        
        try:
            stat = os.stat(store_image_path)
            return {
                "name": image_name,
                "path": store_image_path,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "extension": os.path.splitext(image_name)[1]
            }
        except Exception:
            return None


class ValidationTools:
    """Validates poetry collection integrity."""
    
    def __init__(self, poem_manager: PoemManager):
        self.poem_manager = poem_manager
    
    def validate_collection(self) -> Dict[str, List[str]]:
        """Validate the entire poetry collection."""
        issues = {
            "missing_files": [],
            "invalid_metadata": [],
            "empty_content": [],
            "missing_images": []
        }
        
        poems = self.poem_manager.list_poems()
        
        for poem in poems:
            poem_num = poem["number"]
            
            # Check file existence
            if not os.path.exists(poem["file_path"]):
                issues["missing_files"].append(f"Poem #{poem_num}")
            
            # Check metadata
            metadata = poem["metadata"]
            required_fields = ["title", "author", "language", "form", "length"]
            missing_fields = [field for field in required_fields if not metadata.get(field)]
            if missing_fields:
                issues["invalid_metadata"].append(f"Poem #{poem_num}: missing {', '.join(missing_fields)}")
            
            # Check content
            if not poem["content"].strip():
                issues["empty_content"].append(f"Poem #{poem_num}")
            
            # Check image
            if not poem["has_image"]:
                issues["missing_images"].append(f"Poem #{poem_num}")
        
        return issues
    
    def repair_numbering(self) -> bool:
        """Repair poem numbering to be sequential."""
        poems = self.poem_manager.list_poems()
        if not poems:
            return True
        
        print("🔧 Repairing poem numbering...")
        
        # Sort by current number
        poems.sort(key=lambda x: x["number"])
        
        # Rename to temporary numbers first
        temp_mappings = {}
        for i, poem in enumerate(poems, 1):
            old_num = poem["number"]
            if old_num != i:
                temp_num = f"temp_{i}"
                old_dir = os.path.join("Poetry", str(old_num))
                temp_dir = os.path.join("Poetry", temp_num)
                
                try:
                    os.rename(old_dir, temp_dir)
                    temp_mappings[temp_num] = i
                except Exception as e:
                    print(f"❌ Error renaming {old_num} to {temp_num}: {e}")
                    return False
        
        # Rename from temporary to final numbers
        for temp_num, final_num in temp_mappings.items():
            temp_dir = os.path.join("Poetry", temp_num)
            final_dir = os.path.join("Poetry", str(final_num))
            
            try:
                os.rename(temp_dir, final_dir)
                print(f"✅ Renumbered poem to #{final_num}")
            except Exception as e:
                print(f"❌ Error renaming {temp_num} to {final_num}: {e}")
                return False
        
        print("✅ Poem numbering repaired")
        return True


class PoetryCLI:
    """Main CLI interface for poetry management."""
    
    def __init__(self):
        self.metadata_manager = MetadataManager()
        self.backup_manager = BackupManager()
        self.poem_manager = PoemManager(self.metadata_manager)
        self.image_manager = ImageManager()
        self.validator = ValidationTools(self.poem_manager)
    
    def run(self):
        """Run the main CLI."""
        print("🎭 Poetry Management CLI")
        print("=" * 40)
        print("Welcome to your comprehensive poetry management system!")
        print("=" * 40)
        
        while True:
            self._show_main_menu()
            choice = input("\n📝 Choose an option: ").strip()
            
            if choice == '1':
                self._poems_menu()
            elif choice == '2':
                self._metadata_menu()
            elif choice == '3':
                self._images_menu()
            elif choice == '4':
                self._tools_menu()
            elif choice == '5':
                self._show_statistics()
            elif choice == '6':
                print("👋 Goodbye! Happy writing!")
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _show_main_menu(self):
        """Display the main menu."""
        print(f"\n🏠 Main Menu")
        print("=" * 30)
        print("1. 📝 Manage Poems")
        print("2. 🏷️  Manage Metadata")
        print("3. 🖼️  Manage Images")
        print("4. 🔧 Tools & Validation")
        print("5. 📊 Statistics")
        print("6. 🚪 Exit")
    
    def _poems_menu(self):
        """Poems management menu."""
        while True:
            print(f"\n📝 Poem Management")
            print("=" * 30)
            print("1. ➕ Add New Poem")
            print("2. 📖 View Poem")
            print("3. ✏️  Edit Poem")
            print("4. 🗑️  Delete Poem")
            print("5. 📋 List All Poems")
            print("6. 🔍 Search Poems")
            print("7. ⬅️  Back to Main Menu")
            
            choice = input("\n📝 Choose option: ").strip()
            
            if choice == '1':
                self._add_poem()
            elif choice == '2':
                self._view_poem()
            elif choice == '3':
                self._edit_poem()
            elif choice == '4':
                self._delete_poem()
            elif choice == '5':
                self._list_poems()
            elif choice == '6':
                self._search_poems()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice!")
    
    def _add_poem(self):
        """Add a new poem interactively."""
        print(f"\n➕ Add New Poem")
        print("=" * 30)
        
        # Get title
        title = input("📝 Poem title: ").strip()
        if not title:
            print("❌ Title is required!")
            return
        
        # Get author
        default_author = self.metadata_manager.get_default_author()
        author = input(f"👤 Author (default: {default_author}): ").strip()
        if not author:
            author = default_author
        
        # Get language
        languages = self.metadata_manager.get_languages()
        print(f"\n🌍 Available languages:")
        for i, lang in enumerate(languages, 1):
            print(f"   {i}. {lang['name']} ({lang['code']})")
        
        lang_choice = input("Choose language (number or code): ").strip()
        if lang_choice.isdigit():
            lang_index = int(lang_choice) - 1
            if 0 <= lang_index < len(languages):
                language = languages[lang_index]["code"]
            else:
                language = "en"
        else:
            language = lang_choice if lang_choice in self.metadata_manager.get_language_codes() else "en"
        
        # Get form
        forms = self.metadata_manager.get_forms()
        print(f"\n📚 Available forms:")
        for i, form in enumerate(forms, 1):
            print(f"   {i}. {form}")
        
        form_choice = input("Choose form (number or name): ").strip()
        if form_choice.isdigit():
            form_index = int(form_choice) - 1
            if 0 <= form_index < len(forms):
                form = forms[form_index]
            else:
                form = "Free Verse"
        else:
            form = form_choice if form_choice in forms else "Free Verse"
        
        # Get length
        lengths = self.metadata_manager.get_lengths()
        print(f"\n📏 Available lengths:")
        for i, length in enumerate(lengths, 1):
            print(f"   {i}. {length}")
        
        length_choice = input("Choose length (number or name): ").strip()
        if length_choice.isdigit():
            length_index = int(length_choice) - 1
            if 0 <= length_index < len(lengths):
                length = lengths[length_index]
            else:
                length = "Standard"
        else:
            length = length_choice if length_choice in lengths else "Standard"
        
        # Get content
        print(f"\n📝 Enter poem content (press Enter twice when done):")
        content_lines = []
        empty_count = 0
        
        while True:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                content_lines.append(line)
            else:
                empty_count = 0
                content_lines.append(line)
        
        content = '\n'.join(content_lines).strip()
        if not content:
            print("❌ Poem content is required!")
            return
        
        # Create poem
        poem_number = self.poem_manager.create_poem(
            title=title,
            content=content,
            author=author,
            language=language,
            form=form,
            length=length
        )
        
        if poem_number:
            # Ask about image
            add_image = input(f"\n🖼️  Add an image to poem #{poem_number}? (y/n): ").strip().lower()
            if add_image == 'y':
                image_path = input("📁 Image file path: ").strip()
                if image_path and os.path.exists(image_path):
                    self.image_manager.add_image_to_poem(poem_number, image_path)
                else:
                    print("⚠️  Image file not found, skipping...")
            
            print(f"\n✅ Poem #{poem_number} created successfully!")
    
    def _view_poem(self):
        """View a specific poem."""
        try:
            poem_number = int(input("📖 Enter poem number: ").strip())
            poem_data = self.poem_manager.get_poem(poem_number)
            
            if not poem_data:
                print(f"❌ Poem #{poem_number} not found!")
                return
            
            metadata = poem_data["metadata"]
            print(f"\n📖 Poem #{poem_number}")
            print("=" * 40)
            print(f"Title: {metadata.get('title', 'Unknown')}")
            print(f"Author: {metadata.get('author', 'Unknown')}")
            print(f"Language: {metadata.get('language', 'Unknown')}")
            print(f"Form: {metadata.get('form', 'Unknown')}")
            print(f"Length: {metadata.get('length', 'Unknown')}")
            print(f"Has Image: {'✅' if poem_data['has_image'] else '❌'}")
            print("\nContent:")
            print("-" * 20)
            print(poem_data["content"])
            print("-" * 20)
            
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _edit_poem(self):
        """Edit an existing poem."""
        try:
            poem_number = int(input("✏️  Enter poem number to edit: ").strip())
            poem_data = self.poem_manager.get_poem(poem_number)
            
            if not poem_data:
                print(f"❌ Poem #{poem_number} not found!")
                return
            
            # Create backup first
            self.backup_manager.create_backup(f"Before editing poem #{poem_number}")
            
            metadata = poem_data["metadata"]
            
            print(f"\n✏️  Editing Poem #{poem_number}")
            print("=" * 40)
            print("Press Enter to keep current value")
            
            # Edit metadata
            new_title = input(f"Title ({metadata.get('title', '')}): ").strip()
            new_author = input(f"Author ({metadata.get('author', '')}): ").strip()
            
            # Language selection
            languages = self.metadata_manager.get_languages()
            current_lang = metadata.get('language', 'en')
            print(f"\nCurrent language: {current_lang}")
            print("Available languages:")
            for i, lang in enumerate(languages, 1):
                print(f"   {i}. {lang['name']} ({lang['code']})")
            new_language = input("New language (number/code/Enter to keep): ").strip()
            
            # Form selection
            forms = self.metadata_manager.get_forms()
            current_form = metadata.get('form', 'Free Verse')
            print(f"\nCurrent form: {current_form}")
            print("Available forms:")
            for i, form in enumerate(forms, 1):
                print(f"   {i}. {form}")
            new_form = input("New form (number/name/Enter to keep): ").strip()
            
            # Length selection
            lengths = self.metadata_manager.get_lengths()
            current_length = metadata.get('length', 'Standard')
            print(f"\nCurrent length: {current_length}")
            print("Available lengths:")
            for i, length in enumerate(lengths, 1):
                print(f"   {i}. {length}")
            new_length = input("New length (number/name/Enter to keep): ").strip()
            
            # Content editing
            edit_content = input(f"\nEdit content? (y/n): ").strip().lower()
            new_content = None
            if edit_content == 'y':
                print("Enter new content (press Enter twice when done):")
                content_lines = []
                empty_count = 0
                
                while True:
                    line = input()
                    if line.strip() == "":
                        empty_count += 1
                        if empty_count >= 2:
                            break
                        content_lines.append(line)
                    else:
                        empty_count = 0
                        content_lines.append(line)
                
                new_content = '\n'.join(content_lines).strip()
            
            # Apply updates
            updates = {}
            if new_title:
                updates["title"] = new_title
            if new_author:
                updates["author"] = new_author
            if new_language:
                if new_language.isdigit():
                    lang_index = int(new_language) - 1
                    if 0 <= lang_index < len(languages):
                        updates["language"] = languages[lang_index]["code"]
                else:
                    updates["language"] = new_language
            if new_form:
                if new_form.isdigit():
                    form_index = int(new_form) - 1
                    if 0 <= form_index < len(forms):
                        updates["form"] = forms[form_index]
                else:
                    updates["form"] = new_form
            if new_length:
                if new_length.isdigit():
                    length_index = int(new_length) - 1
                    if 0 <= length_index < len(lengths):
                        updates["length"] = lengths[length_index]
                else:
                    updates["length"] = new_length
            if new_content is not None:
                updates["content"] = new_content
            
            if updates or new_content is not None:
                success = self.poem_manager.update_poem(poem_number, **updates)
                if success:
                    print(f"✅ Poem #{poem_number} updated successfully!")
                else:
                    print(f"❌ Failed to update poem #{poem_number}")
            else:
                print("📝 No changes made")
                
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _delete_poem(self):
        """Delete a poem with confirmation."""
        try:
            poem_number = int(input("🗑️  Enter poem number to delete: ").strip())
            poem_data = self.poem_manager.get_poem(poem_number)
            
            if not poem_data:
                print(f"❌ Poem #{poem_number} not found!")
                return
            
            # Show poem info and confirm
            title = poem_data["metadata"].get("title", f"Poem #{poem_number}")
            print(f"\n⚠️  About to delete:")
            print(f"   Poem #{poem_number}: {title}")
            print(f"   Author: {poem_data['metadata'].get('author', 'Unknown')}")
            print(f"   Has image: {'Yes' if poem_data['has_image'] else 'No'}")
            
            confirm = input(f"\nType 'DELETE' to confirm deletion: ").strip()
            if confirm != 'DELETE':
                print("❌ Deletion cancelled")
                return
            
            # Create backup first
            self.backup_manager.create_backup(f"Before deleting poem #{poem_number}")
            
            # Delete poem
            if self.poem_manager.delete_poem(poem_number):
                print(f"✅ Poem #{poem_number} deleted successfully!")
            else:
                print(f"❌ Failed to delete poem #{poem_number}")
                
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _list_poems(self):
        """List all poems with filtering options."""
        print(f"\n📋 List Poems")
        print("=" * 30)
        
        # Ask for filters
        print("Optional filters (press Enter to skip):")
        filter_language = input("Language: ").strip()
        filter_form = input("Form: ").strip()
        filter_length = input("Length: ").strip()
        filter_author = input("Author: ").strip()
        
        # Build filter dictionary
        filters = {}
        if filter_language:
            filters["language"] = filter_language
        if filter_form:
            filters["form"] = filter_form
        if filter_length:
            filters["length"] = filter_length
        if filter_author:
            filters["author"] = filter_author
        
        # Get poems
        poems = self.poem_manager.list_poems(filters)
        
        if not poems:
            print("📭 No poems found matching your criteria")
            return
        
        print(f"\n📚 Found {len(poems)} poem(s):")
        print("-" * 60)
        
        for poem in poems:
            metadata = poem["metadata"]
            print(f"#{poem['number']:2d} | {metadata.get('title', 'Untitled'):30s} | {metadata.get('author', 'Unknown'):15s} | {metadata.get('form', 'Unknown'):10s} | {'🖼️' if poem['has_image'] else '  '}")
        
        print("-" * 60)
    
    def _search_poems(self):
        """Search poems by content or title."""
        query = input("🔍 Enter search term: ").strip()
        if not query:
            print("❌ Search query is required!")
            return
        
        results = self.poem_manager.search_poems(query)
        
        if not results:
            print(f"📭 No poems found containing '{query}'")
            return
        
        print(f"\n🔍 Found {len(results)} poem(s) containing '{query}':")
        print("-" * 60)
        
        for poem in results:
            metadata = poem["metadata"]
            print(f"#{poem['number']:2d} | {metadata.get('title', 'Untitled'):30s} | {metadata.get('author', 'Unknown'):15s}")
        
        print("-" * 60)
    
    def _metadata_menu(self):
        """Metadata management menu."""
        while True:
            print(f"\n🏷️  Metadata Management")
            print("=" * 30)
            print("1. 📋 View Current Categories")
            print("2. ➕ Add New Form")
            print("3. ➕ Add New Length")
            print("4. ➕ Add New Language")
            print("5. 🗑️  Remove Category")
            print("6. ⬅️  Back to Main Menu")
            
            choice = input("\n🏷️  Choose option: ").strip()
            
            if choice == '1':
                self._view_categories()
            elif choice == '2':
                self._add_form()
            elif choice == '3':
                self._add_length()
            elif choice == '4':
                self._add_language()
            elif choice == '5':
                self._remove_category()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice!")
    
    def _view_categories(self):
        """View all current metadata categories."""
        print(f"\n📋 Current Categories")
        print("=" * 30)
        
        forms = self.metadata_manager.get_forms()
        lengths = self.metadata_manager.get_lengths()
        languages = self.metadata_manager.get_languages()
        
        print(f"📚 Forms ({len(forms)}):")
        for form in forms:
            print(f"   • {form}")
        
        print(f"\n📏 Lengths ({len(lengths)}):")
        for length in lengths:
            print(f"   • {length}")
        
        print(f"\n🌍 Languages ({len(languages)}):")
        for lang in languages:
            print(f"   • {lang['name']} ({lang['code']})")
        
        print(f"\n👤 Default Author: {self.metadata_manager.get_default_author()}")
    
    def _add_form(self):
        """Add a new poetry form."""
        form = input("📚 Enter new form name: ").strip()
        if form:
            self.metadata_manager.add_form(form)
        else:
            print("❌ Form name is required!")
    
    def _add_length(self):
        """Add a new poetry length."""
        length = input("📏 Enter new length name: ").strip()
        if length:
            self.metadata_manager.add_length(length)
        else:
            print("❌ Length name is required!")
    
    def _add_language(self):
        """Add a new language."""
        code = input("🌍 Enter language code (e.g., 'fr'): ").strip().lower()
        name = input("🌍 Enter language name (e.g., 'French'): ").strip()
        
        if code and name:
            self.metadata_manager.add_language(code, name)
        else:
            print("❌ Both code and name are required!")
    
    def _remove_category(self):
        """Remove a metadata category."""
        print(f"\n🗑️  Remove Category")
        print("=" * 30)
        print("1. Remove Form")
        print("2. Remove Length")
        print("3. Cancel")
        
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            forms = self.metadata_manager.get_forms()
            print("Available forms:")
            for i, form in enumerate(forms, 1):
                print(f"   {i}. {form}")
            
            form_choice = input("Enter form name or number to remove: ").strip()
            if form_choice.isdigit():
                form_index = int(form_choice) - 1
                if 0 <= form_index < len(forms):
                    self.metadata_manager.remove_form(forms[form_index])
            else:
                self.metadata_manager.remove_form(form_choice)
        
        elif choice == '2':
            lengths = self.metadata_manager.get_lengths()
            print("Available lengths:")
            for i, length in enumerate(lengths, 1):
                print(f"   {i}. {length}")
            
            length_choice = input("Enter length name or number to remove: ").strip()
            if length_choice.isdigit():
                length_index = int(length_choice) - 1
                if 0 <= length_index < len(lengths):
                    self.metadata_manager.remove_length(lengths[length_index])
            else:
                self.metadata_manager.remove_length(length_choice)
    
    def _images_menu(self):
        """Image management menu."""
        while True:
            print(f"\n🖼️  Image Management")
            print("=" * 30)
            print("1. ➕ Add Image to Poem (from file)")
            print("2. 📦 Add Image to Store")
            print("3. 🔗 Assign Store Image to Poem")
            print("4. 📋 Browse Image Store")
            print("5. 📁 Bulk Add Images to Store")
            print("6. 🗑️  Remove Image from Poem")
            print("7. 🗑️  Delete Image from Store")
            print("8. 📊 List Poems with Images")
            print("9. 📊 List Poems without Images")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\n🖼️  Choose option: ").strip()
            
            if choice == '1':
                self._add_image_direct()
            elif choice == '2':
                self._add_image_to_store()
            elif choice == '3':
                self._assign_store_image()
            elif choice == '4':
                self._browse_image_store()
            elif choice == '5':
                self._bulk_add_images()
            elif choice == '6':
                self._remove_image()
            elif choice == '7':
                self._delete_store_image()
            elif choice == '8':
                self._list_poems_with_images()
            elif choice == '9':
                self._list_poems_without_images()
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
    
    def _add_image_direct(self):
        """Add image directly to a poem from file."""
        try:
            poem_number = int(input("📝 Enter poem number: ").strip())
            image_path = input("📁 Enter image file path: ").strip()
            
            if self.image_manager.add_image_to_poem(poem_number, image_path):
                print(f"✅ Image added to poem #{poem_number}")
            
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _add_image_to_store(self):
        """Add an image to the store."""
        image_path = input("📁 Enter image file path: ").strip()
        if not image_path:
            print("❌ Image path is required!")
            return
        
        name = input("🏷️  Enter name for image (optional): ").strip()
        
        if self.image_manager.add_image_to_store(image_path, name if name else None):
            print("✅ Image added to store successfully!")
    
    def _assign_store_image(self):
        """Assign an image from store to a poem."""
        # First show available images
        images = self.image_manager.list_store_images()
        
        if not images:
            print("📭 No images in store. Add some images first!")
            return
        
        print(f"\n📋 Available Images in Store ({len(images)}):")
        print("-" * 60)
        
        for i, img in enumerate(images[:20], 1):  # Show first 20
            size_kb = round(img["size"] / 1024, 1)
            print(f"{i:2d}. {img['name']:30s} | {size_kb:6.1f}KB | {img['modified']}")
        
        if len(images) > 20:
            print(f"... and {len(images) - 20} more images")
        
        print("-" * 60)
        
        try:
            poem_number = int(input("\n📝 Enter poem number: ").strip())
            image_choice = input("🖼️  Enter image name or number: ").strip()
            
            # Check if it's a number (index) or name
            if image_choice.isdigit():
                img_index = int(image_choice) - 1
                if 0 <= img_index < len(images):
                    image_name = images[img_index]["name"]
                else:
                    print("❌ Invalid image number!")
                    return
            else:
                image_name = image_choice
            
            if self.image_manager.assign_store_image_to_poem(poem_number, image_name):
                print(f"✅ Assigned {image_name} to poem #{poem_number}")
            
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _browse_image_store(self):
        """Browse images in the store."""
        images = self.image_manager.list_store_images()
        
        if not images:
            print("📭 No images in store")
            return
        
        print(f"\n📋 Image Store ({len(images)} images):")
        print("-" * 80)
        print("No. | Name                           | Size      | Modified         | Format")
        print("-" * 80)
        
        total_size = 0
        for i, img in enumerate(images, 1):
            size_kb = round(img["size"] / 1024, 1)
            total_size += img["size"]
            ext = os.path.splitext(img["name"])[1]
            print(f"{i:2d}. | {img['name']:30s} | {size_kb:6.1f}KB | {img['modified']} | {ext}")
        
        print("-" * 80)
        total_mb = round(total_size / (1024 * 1024), 2)
        print(f"Total: {len(images)} images, {total_mb}MB")
        
        # Option to view details of specific image
        view_details = input("\n📖 View details of specific image? (enter name/number or press Enter to skip): ").strip()
        
        if view_details:
            if view_details.isdigit():
                img_index = int(view_details) - 1
                if 0 <= img_index < len(images):
                    self._show_image_details(images[img_index]["name"])
            else:
                self._show_image_details(view_details)
    
    def _show_image_details(self, image_name: str):
        """Show detailed information about an image."""
        info = self.image_manager.get_image_info(image_name)
        
        if not info:
            print(f"❌ Image not found: {image_name}")
            return
        
        print(f"\n📋 Image Details: {image_name}")
        print("=" * 40)
        print(f"Name: {info['name']}")
        print(f"Path: {info['path']}")
        print(f"Size: {info['size']:,} bytes ({info['size_mb']} MB)")
        print(f"Modified: {info['modified']}")
        print(f"Format: {info['extension']}")
    
    def _bulk_add_images(self):
        """Bulk add images from a directory."""
        directory = input("📁 Enter directory path containing images: ").strip()
        
        if not directory:
            print("❌ Directory path is required!")
            return
        
        if not os.path.exists(directory):
            print(f"❌ Directory not found: {directory}")
            return
        
        print(f"🔍 Scanning {directory} for images...")
        count = self.image_manager.bulk_add_images_to_store(directory)
        
        if count > 0:
            print(f"✅ Successfully added {count} images to store!")
        else:
            print("📭 No images found in directory")
    
    def _delete_store_image(self):
        """Delete an image from the store."""
        images = self.image_manager.list_store_images()
        
        if not images:
            print("📭 No images in store")
            return
        
        print(f"\n📋 Images in Store ({len(images)}):")
        print("-" * 50)
        
        for i, img in enumerate(images[:10], 1):  # Show first 10
            size_kb = round(img["size"] / 1024, 1)
            print(f"{i:2d}. {img['name']:30s} | {size_kb:6.1f}KB")
        
        if len(images) > 10:
            print(f"... and {len(images) - 10} more images")
        
        print("-" * 50)
        
        image_choice = input("🗑️  Enter image name or number to delete: ").strip()
        
        if image_choice.isdigit():
            img_index = int(image_choice) - 1
            if 0 <= img_index < len(images):
                image_name = images[img_index]["name"]
            else:
                print("❌ Invalid image number!")
                return
        else:
            image_name = image_choice
        
        # Confirm deletion
        confirm = input(f"⚠️  Delete '{image_name}'? Type 'DELETE' to confirm: ").strip()
        if confirm == 'DELETE':
            if self.image_manager.delete_store_image(image_name):
                print(f"✅ Deleted {image_name} from store")
        else:
            print("❌ Deletion cancelled")
    
    def _remove_image(self):
        """Remove image from a poem."""
        try:
            poem_number = int(input("📝 Enter poem number: ").strip())
            
            if self.image_manager.remove_image_from_poem(poem_number):
                print(f"✅ Image removed from poem #{poem_number}")
            
        except ValueError:
            print("❌ Please enter a valid poem number!")
    
    def _list_poems_with_images(self):
        """List poems that have images."""
        poems = self.poem_manager.list_poems()
        poems_with_images = [p for p in poems if p["has_image"]]
        
        if not poems_with_images:
            print("📭 No poems with images found")
            return
        
        print(f"\n🖼️  Poems with Images ({len(poems_with_images)}):")
        print("-" * 50)
        
        for poem in poems_with_images:
            metadata = poem["metadata"]
            print(f"#{poem['number']:2d} | {metadata.get('title', 'Untitled'):30s} | {metadata.get('author', 'Unknown'):15s}")
        
        print("-" * 50)
    
    def _list_poems_without_images(self):
        """List poems that don't have images."""
        poems = self.poem_manager.list_poems()
        poems_without_images = [p for p in poems if not p["has_image"]]
        
        if not poems_without_images:
            print("📭 All poems have images!")
            return
        
        print(f"\n📝 Poems without Images ({len(poems_without_images)}):")
        print("-" * 50)
        
        for poem in poems_without_images:
            metadata = poem["metadata"]
            print(f"#{poem['number']:2d} | {metadata.get('title', 'Untitled'):30s} | {metadata.get('author', 'Unknown'):15s}")
        
        print("-" * 50)
    
    def _tools_menu(self):
        """Tools and validation menu."""
        while True:
            print(f"\n🔧 Tools & Validation")
            print("=" * 30)
            print("1. 🔍 Validate Collection")
            print("2. 📦 Create Backup")
            print("3. 🔄 Restore from Backup")
            print("4. 📋 List Backups")
            print("5. 🔧 Repair Numbering")
            print("6. ⬅️  Back to Main Menu")
            
            choice = input("\n🔧 Choose option: ").strip()
            
            if choice == '1':
                self._validate_collection()
            elif choice == '2':
                self._create_backup()
            elif choice == '3':
                self._restore_backup()
            elif choice == '4':
                self._list_backups()
            elif choice == '5':
                self._repair_numbering()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice!")
    
    def _validate_collection(self):
        """Validate the poetry collection."""
        print(f"\n🔍 Validating Collection...")
        issues = self.validator.validate_collection()
        
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        
        if total_issues == 0:
            print("✅ Collection validation passed! No issues found.")
        else:
            print(f"⚠️  Found {total_issues} issues:")
            
            for issue_type, issue_list in issues.items():
                if issue_list:
                    print(f"\n{issue_type.replace('_', ' ').title()}:")
                    for issue in issue_list:
                        print(f"   • {issue}")
    
    def _create_backup(self):
        """Create a manual backup."""
        description = input("📝 Backup description (optional): ").strip()
        if not description:
            description = "Manual backup"
        
        backup_name = self.backup_manager.create_backup(description)
        if backup_name:
            print(f"✅ Backup created: {backup_name}")
    
    def _restore_backup(self):
        """Restore from a backup."""
        backups = self.backup_manager.list_backups()
        
        if not backups:
            print("📭 No backups available")
            return
        
        print(f"\n📦 Available Backups:")
        print("-" * 60)
        
        for i, backup in enumerate(backups, 1):
            print(f"{i:2d}. {backup['name']:20s} | {backup['description']:20s} | {backup['timestamp']}")
        
        print("-" * 60)
        
        try:
            choice = int(input("Enter backup number to restore: ").strip())
            if 1 <= choice <= len(backups):
                backup_name = backups[choice - 1]["name"]
                
                confirm = input(f"⚠️  This will replace your current collection with '{backup_name}'. Type 'RESTORE' to confirm: ").strip()
                if confirm == 'RESTORE':
                    if self.backup_manager.restore_backup(backup_name):
                        print("✅ Collection restored successfully!")
                    else:
                        print("❌ Restore failed!")
                else:
                    print("❌ Restore cancelled")
            else:
                print("❌ Invalid backup number!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def _list_backups(self):
        """List all available backups."""
        backups = self.backup_manager.list_backups()
        
        if not backups:
            print("📭 No backups available")
            return
        
        print(f"\n📦 Available Backups ({len(backups)}):")
        print("-" * 80)
        print("No. | Name                 | Description          | Date & Time       | Poems")
        print("-" * 80)
        
        for i, backup in enumerate(backups, 1):
            poems_count = backup.get('poems_count', 'Unknown')
            print(f"{i:2d}. | {backup['name']:20s} | {backup['description']:20s} | {backup['timestamp'][:16]} | {poems_count}")
        
        print("-" * 80)
    
    def _repair_numbering(self):
        """Repair poem numbering."""
        print(f"\n🔧 Repair Poem Numbering")
        print("This will renumber poems to be sequential (1, 2, 3, ...)")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm == 'y':
            # Create backup first
            self.backup_manager.create_backup("Before numbering repair")
            
            if self.validator.repair_numbering():
                print("✅ Poem numbering repaired successfully!")
            else:
                print("❌ Numbering repair failed!")
        else:
            print("❌ Repair cancelled")
    
    def _show_statistics(self):
        """Show collection statistics."""
        poems = self.poem_manager.list_poems()
        
        if not poems:
            print("📭 No poems found in collection")
            return
        
        print(f"\n📊 Collection Statistics")
        print("=" * 40)
        
        # Basic counts
        total_poems = len(poems)
        poems_with_images = sum(1 for p in poems if p["has_image"])
        poems_without_images = total_poems - poems_with_images
        
        print(f"Total Poems: {total_poems}")
        print(f"Poems with Images: {poems_with_images}")
        print(f"Poems without Images: {poems_without_images}")
        print(f"Image Coverage: {(poems_with_images/total_poems*100):.1f}%")
        
        # Language breakdown
        languages = {}
        for poem in poems:
            lang = poem["metadata"].get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
        
        print(f"\nBy Language:")
        for lang, count in sorted(languages.items()):
            print(f"   {lang}: {count}")
        
        # Form breakdown
        forms = {}
        for poem in poems:
            form = poem["metadata"].get("form", "unknown")
            forms[form] = forms.get(form, 0) + 1
        
        print(f"\nBy Form:")
        for form, count in sorted(forms.items()):
            print(f"   {form}: {count}")
        
        # Length breakdown
        lengths = {}
        for poem in poems:
            length = poem["metadata"].get("length", "unknown")
            lengths[length] = lengths.get(length, 0) + 1
        
        print(f"\nBy Length:")
        for length, count in sorted(lengths.items()):
            print(f"   {length}: {count}")
        
        # Author breakdown
        authors = {}
        for poem in poems:
            author = poem["metadata"].get("author", "Unknown")
            authors[author] = authors.get(author, 0) + 1
        
        print(f"\nBy Author:")
        for author, count in sorted(authors.items()):
            print(f"   {author}: {count}")


if __name__ == "__main__":
    try:
        cli = PoetryCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy writing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue if it persists.")