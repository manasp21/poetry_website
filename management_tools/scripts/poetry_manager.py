#!/usr/bin/env python3
"""
Comprehensive Poetry Management System
=====================================

A complete solution for managing poetry content with ID-based linking,
safe migration tools, and advanced management features.

Features:
- ID-based poem and image linking
- Safe migration from title-based to ID-based system
- Manual and automatic image assignment
- Bulk operations and metadata management
- Consistency validation and testing
- JavaScript integration and path updates
- Complete backup and rollback capabilities
"""

import os
import json
import re
import shutil
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml


class PoemRegistry:
    """Manages the central poem registry system."""
    
    def __init__(self, registry_path: str = "poem_registry.json"):
        self.registry_path = registry_path
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load existing registry or create new one."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"⚠️  Warning: Could not load registry from {self.registry_path}")
        
        return {
            "poems": {},
            "images": {},
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_poems": 0,
                "total_images": 0
            }
        }
    
    def save_registry(self) -> bool:
        """Save registry to file with backup."""
        try:
            # Create backup if registry exists
            if os.path.exists(self.registry_path):
                backup_path = f"{self.registry_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(self.registry_path, backup_path)
                print(f"📁 Created registry backup: {backup_path}")
            
            # Update metadata
            self.registry["metadata"]["last_updated"] = datetime.now().isoformat()
            self.registry["metadata"]["total_poems"] = len(self.registry["poems"])
            self.registry["metadata"]["total_images"] = len(self.registry["images"])
            
            # Save registry
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Registry saved: {self.registry_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving registry: {e}")
            return False
    
    def get_next_poem_id(self) -> str:
        """Get next available poem ID."""
        existing_ids = [int(pid.replace('poem', '')) for pid in self.registry["poems"].keys() 
                       if pid.startswith('poem') and pid[4:].isdigit()]
        next_id = max(existing_ids, default=0) + 1
        return f"poem{next_id:03d}"
    
    def get_next_image_id(self) -> str:
        """Get next available image ID."""
        existing_ids = [int(iid.replace('image', '')) for iid in self.registry["images"].keys() 
                       if iid.startswith('image') and iid[5:].isdigit()]
        next_id = max(existing_ids, default=0) + 1
        return f"image{next_id:03d}"
    
    def add_poem(self, poem_id: str, metadata: Dict[str, Any]) -> bool:
        """Add poem to registry."""
        if poem_id in self.registry["poems"]:
            print(f"⚠️  Warning: Poem {poem_id} already exists in registry")
            return False
        
        self.registry["poems"][poem_id] = {
            **metadata,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        return True
    
    def add_image(self, image_id: str, metadata: Dict[str, Any]) -> bool:
        """Add image to registry."""
        if image_id in self.registry["images"]:
            print(f"⚠️  Warning: Image {image_id} already exists in registry")
            return False
        
        self.registry["images"][image_id] = metadata
        return True
    
    def link_poem_image(self, poem_id: str, image_id: str) -> bool:
        """Link poem and image."""
        if poem_id not in self.registry["poems"]:
            print(f"❌ Poem {poem_id} not found in registry")
            return False
        
        if image_id not in self.registry["images"]:
            print(f"❌ Image {image_id} not found in registry")
            return False
        
        # Update poem registry
        self.registry["poems"][poem_id]["image_id"] = image_id
        self.registry["poems"][poem_id]["last_modified"] = datetime.now().isoformat()
        
        # Update image registry
        self.registry["images"][image_id]["linked_poem"] = poem_id
        
        print(f"🔗 Linked {poem_id} ↔ {image_id}")
        return True


class PoemMigrator:
    """Handles safe migration from title-based to ID-based system."""
    
    def __init__(self, registry: PoemRegistry):
        self.registry = registry
        self.backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Define poetry directories
        self.poetry_dirs = [
            'Poetry/by_language/english/lengths/short/',
            'Poetry/by_language/english/forms/free_verse/',
            'Poetry/by_language/english/forms/sonnet/',
            'Poetry/by_language/hindi/lengths/standard/'
        ]
        
        self.image_dir = 'assets/images/poems/'
    
    def create_backup(self) -> bool:
        """Create complete backup of current state."""
        try:
            print(f"📦 Creating backup in {self.backup_dir}...")
            
            # Create backup directory
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Backup Poetry directory
            if os.path.exists('Poetry'):
                shutil.copytree('Poetry', os.path.join(self.backup_dir, 'Poetry'))
                print("✅ Backed up Poetry directory")
            
            # Backup images
            if os.path.exists(self.image_dir):
                shutil.copytree(self.image_dir, os.path.join(self.backup_dir, 'images'))
                print("✅ Backed up images directory")
            
            # Backup JavaScript files
            js_files = ['js/content-loader.js', 'js/dynamic-poem-loader.js']
            js_backup_dir = os.path.join(self.backup_dir, 'js')
            os.makedirs(js_backup_dir, exist_ok=True)
            
            for js_file in js_files:
                if os.path.exists(js_file):
                    shutil.copy2(js_file, js_backup_dir)
                    print(f"✅ Backed up {js_file}")
            
            # Save backup manifest
            manifest = {
                "backup_date": datetime.now().isoformat(),
                "backed_up_dirs": ["Poetry", "images", "js"],
                "total_poems": self._count_existing_poems(),
                "total_images": self._count_existing_images()
            }
            
            with open(os.path.join(self.backup_dir, 'backup_manifest.json'), 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✅ Backup completed: {self.backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def _count_existing_poems(self) -> int:
        """Count existing poem files."""
        count = 0
        for poetry_dir in self.poetry_dirs:
            if os.path.exists(poetry_dir):
                count += len(glob.glob(os.path.join(poetry_dir, "*.md")))
        return count
    
    def _count_existing_images(self) -> int:
        """Count existing image files."""
        if os.path.exists(self.image_dir):
            return len(glob.glob(os.path.join(self.image_dir, "*.png")))
        return 0
    
    def analyze_current_structure(self) -> Dict[str, Any]:
        """Analyze current poetry structure before migration."""
        analysis = {
            "poems": [],
            "images": [],
            "orphaned_images": [],
            "poems_without_images": [],
            "total_poems": 0,
            "total_images": 0
        }
        
        print("🔍 Analyzing current structure...")
        
        # Analyze poems
        for poetry_dir in self.poetry_dirs:
            if not os.path.exists(poetry_dir):
                continue
                
            for poem_file in glob.glob(os.path.join(poetry_dir, "*.md")):
                try:
                    with open(poem_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse frontmatter
                    frontmatter, poem_content = self._parse_poem_file(content)
                    
                    poem_info = {
                        "file_path": poem_file,
                        "title": frontmatter.get("title", "Unknown"),
                        "author": frontmatter.get("author", "Unknown"),
                        "image": frontmatter.get("image", ""),
                        "language": frontmatter.get("language", "unknown"),
                        "form": frontmatter.get("form", "unknown"),
                        "length": frontmatter.get("length", "unknown"),
                        "category_path": self._get_category_path(poem_file),
                        "content": poem_content
                    }
                    
                    analysis["poems"].append(poem_info)
                    
                    if not poem_info["image"]:
                        analysis["poems_without_images"].append(poem_info)
                    
                except Exception as e:
                    print(f"⚠️  Error analyzing {poem_file}: {e}")
        
        analysis["total_poems"] = len(analysis["poems"])
        
        # Analyze images
        if os.path.exists(self.image_dir):
            for image_file in glob.glob(os.path.join(self.image_dir, "*.png")):
                image_name = os.path.basename(image_file)
                analysis["images"].append(image_name)
                
                # Check if image is referenced by any poem
                is_referenced = any(poem["image"] == image_name for poem in analysis["poems"])
                if not is_referenced:
                    analysis["orphaned_images"].append(image_name)
        
        analysis["total_images"] = len(analysis["images"])
        
        # Print analysis summary
        print(f"📊 Analysis Results:")
        print(f"   Total Poems: {analysis['total_poems']}")
        print(f"   Total Images: {analysis['total_images']}")
        print(f"   Poems without images: {len(analysis['poems_without_images'])}")
        print(f"   Orphaned images: {len(analysis['orphaned_images'])}")
        
        return analysis
    
    def _parse_poem_file(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter and poem content."""
        frontmatter = {}
        poem_content = content.strip()
        
        # Extract frontmatter
        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    poem_content = parts[2].strip()
                except yaml.YAMLError:
                    # Fallback to simple parsing
                    frontmatter_text = parts[1]
                    for line in frontmatter_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            frontmatter[key] = value
                    poem_content = parts[2].strip()
        
        return frontmatter, poem_content
    
    def _get_category_path(self, file_path: str) -> str:
        """Extract category path from file path."""
        path_parts = Path(file_path).parts
        if 'by_language' in path_parts:
            lang_index = path_parts.index('by_language')
            if lang_index + 3 < len(path_parts):
                return f"{path_parts[lang_index + 1]}/{path_parts[lang_index + 2]}/{path_parts[lang_index + 3]}"
        return "unknown/unknown/unknown"
    
    def generate_registry_from_current(self) -> bool:
        """Generate registry from current structure without moving files."""
        print("📝 Generating registry from current structure...")
        
        analysis = self.analyze_current_structure()
        
        # Process poems
        for i, poem_info in enumerate(analysis["poems"], 1):
            poem_id = f"poem{i:03d}"
            
            # Add poem to registry
            poem_metadata = {
                "title": poem_info["title"],
                "author": poem_info["author"],
                "original_filename": os.path.basename(poem_info["file_path"]),
                "language": poem_info["language"],
                "form": poem_info["form"],
                "length": poem_info["length"],
                "category_path": poem_info["category_path"],
                "content": poem_info["content"],
                "original_path": poem_info["file_path"]
            }
            
            self.registry.add_poem(poem_id, poem_metadata)
            
            # Handle image if present
            if poem_info["image"]:
                # Find or create image ID
                image_id = None
                for existing_image_id, existing_image_data in self.registry.registry["images"].items():
                    if existing_image_data.get("original_filename") == poem_info["image"]:
                        image_id = existing_image_id
                        break
                
                if not image_id:
                    image_id = self.registry.get_next_image_id()
                    self.registry.add_image(image_id, {
                        "original_filename": poem_info["image"],
                        "file_extension": ".png"
                    })
                
                # Link poem and image
                self.registry.link_poem_image(poem_id, image_id)
        
        # Add orphaned images
        for orphaned_image in analysis["orphaned_images"]:
            image_id = self.registry.get_next_image_id()
            self.registry.add_image(image_id, {
                "original_filename": orphaned_image,
                "file_extension": ".png",
                "linked_poem": None
            })
        
        print(f"✅ Generated registry with {len(self.registry.registry['poems'])} poems and {len(self.registry.registry['images'])} images")
        return self.registry.save_registry()
    
    def perform_migration(self) -> bool:
        """Perform the actual migration to ID-based system."""
        print("🚀 Starting migration to ID-based system...")
        
        try:
            # Phase 1: Migrate poem files
            print("\n📝 Phase 1: Migrating poem files...")
            for poem_id, poem_data in self.registry.registry["poems"].items():
                old_path = poem_data.get("original_path")
                if not old_path or not os.path.exists(old_path):
                    print(f"⚠️  Skipping {poem_id}: original file not found")
                    continue
                
                new_path = f"Poetry/{poem_id}.md"
                
                # Create content with updated image reference
                content = self._create_updated_poem_content(poem_data)
                
                # Write new file
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Migrated: {os.path.basename(old_path)} -> {poem_id}.md")
            
            # Phase 2: Migrate image files
            print("\n🖼️  Phase 2: Migrating image files...")
            for image_id, image_data in self.registry.registry["images"].items():
                old_filename = image_data.get("original_filename")
                if not old_filename:
                    continue
                
                old_path = os.path.join(self.image_dir, old_filename)
                new_path = os.path.join(self.image_dir, f"{image_id}.png")
                
                if os.path.exists(old_path):
                    shutil.move(old_path, new_path)
                    print(f"✅ Migrated: {old_filename} -> {image_id}.png")
                else:
                    print(f"⚠️  Image not found: {old_filename}")
            
            # Phase 3: Clean up old poem files
            print("\n🧹 Phase 3: Cleaning up old files...")
            for poem_id, poem_data in self.registry.registry["poems"].items():
                old_path = poem_data.get("original_path")
                if old_path and os.path.exists(old_path):
                    os.remove(old_path)
                    print(f"🗑️  Removed: {old_path}")
            
            print("\n✅ Migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            print("💡 Use rollback function to restore from backup.")
            return False
    
    def _create_updated_poem_content(self, poem_data: Dict[str, Any]) -> str:
        """Create updated poem content with new image reference."""
        # Create frontmatter
        frontmatter = {
            "title": poem_data.get("title", "Untitled"),
            "author": poem_data.get("author", "Unknown Author"),
            "language": poem_data.get("language", "en"),
            "form": poem_data.get("form", "unknown"),
            "length": poem_data.get("length", "unknown")
        }
        
        # Add image reference if exists
        if "image_id" in poem_data:
            frontmatter["image"] = f"{poem_data['image_id']}.png"
        
        # Create YAML frontmatter
        yaml_content = "---\n"
        for key, value in frontmatter.items():
            yaml_content += f'{key}: "{value}"\n'
        yaml_content += "---\n"
        
        # Add poem content
        poem_content = poem_data.get("content", "")
        
        return yaml_content + poem_content
    
    def rollback_migration(self) -> bool:
        """Rollback migration using backup."""
        if not os.path.exists(self.backup_dir):
            print(f"❌ Backup directory not found: {self.backup_dir}")
            return False
        
        try:
            print(f"🔄 Rolling back from backup: {self.backup_dir}")
            
            # Restore Poetry directory
            if os.path.exists('Poetry'):
                shutil.rmtree('Poetry')
            
            backup_poetry = os.path.join(self.backup_dir, 'Poetry')
            if os.path.exists(backup_poetry):
                shutil.copytree(backup_poetry, 'Poetry')
                print("✅ Restored Poetry directory")
            
            # Restore images
            if os.path.exists(self.image_dir):
                shutil.rmtree(self.image_dir)
            
            backup_images = os.path.join(self.backup_dir, 'images')
            if os.path.exists(backup_images):
                os.makedirs(os.path.dirname(self.image_dir), exist_ok=True)
                shutil.copytree(backup_images, self.image_dir)
                print("✅ Restored images directory")
            
            # Restore JavaScript files
            js_backup_dir = os.path.join(self.backup_dir, 'js')
            if os.path.exists(js_backup_dir):
                for js_file in os.listdir(js_backup_dir):
                    src = os.path.join(js_backup_dir, js_file)
                    dst = os.path.join('js', js_file)
                    shutil.copy2(src, dst)
                    print(f"✅ Restored {js_file}")
            
            print("✅ Rollback completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False


class ValidationTools:
    """Tools for consistency validation and testing."""
    
    def __init__(self, registry: PoemRegistry):
        self.registry = registry
    
    def validate_registry_integrity(self) -> Dict[str, List[str]]:
        """Validate registry data integrity."""
        issues = {
            "missing_poems": [],
            "missing_images": [],
            "broken_links": [],
            "duplicate_titles": [],
            "missing_metadata": []
        }
        
        print("🔍 Validating registry integrity...")
        
        # Check for missing poem files
        for poem_id, poem_data in self.registry.registry["poems"].items():
            expected_path = f"Poetry/{poem_id}.md"
            if not os.path.exists(expected_path):
                issues["missing_poems"].append(f"{poem_id} -> {expected_path}")
        
        # Check for missing image files
        for image_id, image_data in self.registry.registry["images"].items():
            expected_path = f"assets/images/poems/{image_id}.png"
            if not os.path.exists(expected_path):
                issues["missing_images"].append(f"{image_id} -> {expected_path}")
        
        # Check for broken poem-image links
        for poem_id, poem_data in self.registry.registry["poems"].items():
            if "image_id" in poem_data:
                image_id = poem_data["image_id"]
                if image_id not in self.registry.registry["images"]:
                    issues["broken_links"].append(f"{poem_id} -> {image_id} (image not found)")
        
        # Check for duplicate titles
        titles = {}
        for poem_id, poem_data in self.registry.registry["poems"].items():
            title = poem_data.get("title", "")
            if title in titles:
                issues["duplicate_titles"].append(f"'{title}': {titles[title]} and {poem_id}")
            else:
                titles[title] = poem_id
        
        # Check for missing essential metadata
        required_fields = ["title", "author", "language", "form", "length"]
        for poem_id, poem_data in self.registry.registry["poems"].items():
            missing_fields = [field for field in required_fields if not poem_data.get(field)]
            if missing_fields:
                issues["missing_metadata"].append(f"{poem_id}: missing {', '.join(missing_fields)}")
        
        # Print validation results
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        if total_issues == 0:
            print("✅ Registry validation passed - no issues found")
        else:
            print(f"⚠️  Found {total_issues} validation issues:")
            for issue_type, issue_list in issues.items():
                if issue_list:
                    print(f"   {issue_type.replace('_', ' ').title()}: {len(issue_list)}")
                    for issue in issue_list[:3]:  # Show first 3 issues
                        print(f"     - {issue}")
                    if len(issue_list) > 3:
                        print(f"     ... and {len(issue_list) - 3} more")
        
        return issues
    
    def test_website_functionality(self) -> bool:
        """Test if website will function correctly after migration."""
        print("🌐 Testing website functionality...")
        
        # Test 1: Check if all poems can be loaded
        print("  📝 Testing poem loading...")
        loadable_poems = 0
        for poem_id in self.registry.registry["poems"]:
            poem_path = f"Poetry/{poem_id}.md"
            if os.path.exists(poem_path):
                try:
                    with open(poem_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if content.strip():
                        loadable_poems += 1
                except Exception:
                    pass
        
        total_poems = len(self.registry.registry["poems"])
        poem_load_rate = (loadable_poems / total_poems * 100) if total_poems > 0 else 0
        print(f"     Poems loadable: {loadable_poems}/{total_poems} ({poem_load_rate:.1f}%)")
        
        # Test 2: Check image availability
        print("  🖼️  Testing image availability...")
        available_images = 0
        for image_id in self.registry.registry["images"]:
            image_path = f"assets/images/poems/{image_id}.png"
            if os.path.exists(image_path):
                available_images += 1
        
        total_images = len(self.registry.registry["images"])
        image_availability_rate = (available_images / total_images * 100) if total_images > 0 else 0
        print(f"     Images available: {available_images}/{total_images} ({image_availability_rate:.1f}%)")
        
        # Test 3: Check JavaScript compatibility
        print("  📜 Testing JavaScript compatibility...")
        js_paths_valid = self._test_js_paths()
        
        # Overall assessment
        all_tests_passed = (poem_load_rate >= 95 and 
                           image_availability_rate >= 90 and 
                           js_paths_valid)
        
        if all_tests_passed:
            print("✅ All website functionality tests passed")
        else:
            print("⚠️  Some website functionality tests failed - review before deployment")
        
        return all_tests_passed
    
    def _test_js_paths(self) -> bool:
        """Test if JavaScript files have valid paths."""
        try:
            # Check if content-loader.js exists and has valid structure
            if os.path.exists('js/content-loader.js'):
                with open('js/content-loader.js', 'r', encoding='utf-8') as f:
                    js_content = f.read()
                
                # Basic check for expected structure
                if 'fetchAllPoems' in js_content and 'parsePoemFileContent' in js_content:
                    print("     JavaScript structure: ✅")
                    return True
                else:
                    print("     JavaScript structure: ❌ Missing expected functions")
                    return False
            else:
                print("     JavaScript structure: ❌ content-loader.js not found")
                return False
        except Exception as e:
            print(f"     JavaScript structure: ❌ Error reading JS files: {e}")
            return False


class ImageManager:
    """Manages image operations and assignments."""
    
    def __init__(self, registry: PoemRegistry):
        self.registry = registry
        self.image_dir = 'assets/images/poems/'
    
    def list_unassigned_images(self) -> List[str]:
        """List images that are not linked to any poem."""
        unassigned = []
        for image_id, image_data in self.registry.registry["images"].items():
            if not image_data.get("linked_poem"):
                unassigned.append(image_id)
        return unassigned
    
    def list_poems_without_images(self) -> List[str]:
        """List poems that don't have an assigned image."""
        without_images = []
        for poem_id, poem_data in self.registry.registry["poems"].items():
            if not poem_data.get("image_id"):
                without_images.append(poem_id)
        return without_images
    
    def manual_image_assignment_interface(self):
        """Interactive interface for manual image assignment."""
        print("\n🖼️ Manual Image Assignment Interface")
        print("=" * 40)
        
        poems_without_images = self.list_poems_without_images()
        unassigned_images = self.list_unassigned_images()
        
        if not poems_without_images:
            print("✅ All poems have assigned images!")
            return
        
        if not unassigned_images:
            print("❌ No unassigned images available!")
            return
        
        print(f"Found {len(poems_without_images)} poems without images")
        print(f"Found {len(unassigned_images)} unassigned images")
        
        for poem_id in poems_without_images:
            poem_data = self.registry.registry["poems"][poem_id]
            print(f"\n📝 Poem: {poem_id}")
            print(f"   Title: {poem_data.get('title', 'Unknown')}")
            print(f"   Author: {poem_data.get('author', 'Unknown')}")
            
            # Show first few lines of poem
            content = poem_data.get('content', '')
            first_lines = '\n'.join(content.split('\n')[:3])
            print(f"   Preview: {first_lines[:100]}...")
            
            print(f"\n🖼️ Available images:")
            for i, image_id in enumerate(unassigned_images[:10], 1):
                image_data = self.registry.registry["images"][image_id]
                original_name = image_data.get("original_filename", "unknown")
                print(f"   {i}. {image_id} (was: {original_name})")
            
            if len(unassigned_images) > 10:
                print(f"   ... and {len(unassigned_images) - 10} more")
            
            # Get user choice
            choice = input(f"\nAssign image to '{poem_data.get('title', poem_id)}'? (number/skip/quit): ").strip().lower()
            
            if choice == 'quit':
                break
            elif choice == 'skip':
                continue
            elif choice.isdigit():
                image_index = int(choice) - 1
                if 0 <= image_index < len(unassigned_images):
                    image_id = unassigned_images[image_index]
                    if self.registry.link_poem_image(poem_id, image_id):
                        unassigned_images.remove(image_id)
                        print(f"✅ Assigned {image_id} to {poem_id}")
                    else:
                        print("❌ Failed to assign image")
                else:
                    print("❌ Invalid image number")
            else:
                print("❌ Invalid input")
        
        self.registry.save_registry()
    
    def auto_suggest_image_assignments(self) -> Dict[str, str]:
        """Auto-suggest image assignments based on title similarity."""
        suggestions = {}
        poems_without_images = self.list_poems_without_images()
        unassigned_images = self.list_unassigned_images()
        
        for poem_id in poems_without_images:
            poem_data = self.registry.registry["poems"][poem_id]
            poem_title = poem_data.get("title", "").lower()
            
            best_match = None
            best_score = 0
            
            for image_id in unassigned_images:
                image_data = self.registry.registry["images"][image_id]
                original_name = image_data.get("original_filename", "").lower()
                
                # Simple similarity scoring
                score = self._calculate_title_similarity(poem_title, original_name)
                if score > best_score and score > 0.3:  # Minimum threshold
                    best_score = score
                    best_match = image_id
            
            if best_match:
                suggestions[poem_id] = best_match
        
        return suggestions
    
    def _calculate_title_similarity(self, title: str, filename: str) -> float:
        """Calculate similarity between poem title and image filename."""
        # Remove common words and punctuation
        title_words = set(re.findall(r'\w+', title.lower()))
        filename_words = set(re.findall(r'\w+', filename.lower().replace('-', ' ')))
        
        if not title_words or not filename_words:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = title_words.intersection(filename_words)
        union = title_words.union(filename_words)
        
        return len(intersection) / len(union) if union else 0.0


class JavaScriptUpdater:
    """Updates JavaScript files with new poem paths."""
    
    def __init__(self, registry: PoemRegistry):
        self.registry = registry
    
    def update_content_loader(self) -> bool:
        """Update content-loader.js with new poem paths."""
        try:
            # Generate new paths array
            new_paths = []
            for poem_id in sorted(self.registry.registry["poems"].keys()):
                new_paths.append(f"Poetry/{poem_id}.md")
            
            # Read current content-loader.js
            js_file = 'js/content-loader.js'
            if not os.path.exists(js_file):
                print(f"❌ JavaScript file not found: {js_file}")
                return False
            
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new paths array string
            paths_array = '[\n'
            for path in new_paths:
                paths_array += f'        "{path}",\n'
            paths_array = paths_array.rstrip(',\n') + '\n    ]'
            
            # Replace the old paths array
            pattern = r'const poemFilePaths = \[[\s\S]*?\];'
            new_content = re.sub(
                pattern,
                f'const poemFilePaths = {paths_array};',
                content,
                count=1
            )
            
            if new_content == content:
                print("⚠️  Could not find poemFilePaths array to update")
                return False
            
            # Write updated content
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated {js_file} with {len(new_paths)} poem paths")
            return True
            
        except Exception as e:
            print(f"❌ Error updating content-loader.js: {e}")
            return False
    
    def update_dynamic_loader(self) -> bool:
        """Update dynamic-poem-loader.js fallback paths."""
        try:
            # Generate new paths
            new_paths = []
            for poem_id in sorted(self.registry.registry["poems"].keys()):
                new_paths.append(f"Poetry/{poem_id}.md")
            
            js_file = 'js/dynamic-poem-loader.js'
            if not os.path.exists(js_file):
                print(f"❌ JavaScript file not found: {js_file}")
                return False
            
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new paths array string
            paths_array = '[\n'
            for path in new_paths:
                paths_array += f'        "{path}",\n'
            paths_array = paths_array.rstrip(',\n') + '\n    ]'
            
            # Replace the staticPaths array
            pattern = r'const staticPaths = \[[\s\S]*?\];'
            new_content = re.sub(
                pattern,
                f'const staticPaths = {paths_array};',
                content,
                count=1
            )
            
            if new_content == content:
                print("⚠️  Could not find staticPaths array to update")
                return False
            
            # Write updated content
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated {js_file} with {len(new_paths)} fallback paths")
            return True
            
        except Exception as e:
            print(f"❌ Error updating dynamic-poem-loader.js: {e}")
            return False


class PoetryManagerCLI:
    """Command-line interface for poetry management."""
    
    def __init__(self):
        self.registry = PoemRegistry()
        self.migrator = PoemMigrator(self.registry)
        self.image_manager = ImageManager(self.registry)
        self.js_updater = JavaScriptUpdater(self.registry)
        self.validator = ValidationTools(self.registry)
    
    def run(self):
        """Run the main CLI interface."""
        print("🎭 Comprehensive Poetry Management System")
        print("=" * 50)
        print("⚠️  This is a powerful tool that can modify your entire poetry collection.")
        print("⚠️  Always create backups before running migration operations.")
        print("=" * 50)
        
        while True:
            self._show_main_menu()
            choice = input("\nChoose an option: ").strip()
            
            if choice == '1':
                self._migration_menu()
            elif choice == '2':
                self._image_management_menu()
            elif choice == '3':
                self._validation_menu()
            elif choice == '4':
                self._bulk_operations_menu()
            elif choice == '5':
                self._system_info()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _show_main_menu(self):
        """Show the main menu."""
        print(f"\n🏠 Main Menu")
        print("=" * 30)
        print("1. 🚀 Migration Operations")
        print("2. 🖼️  Image Management")
        print("3. 🔍 Validation & Testing")
        print("4. 📦 Bulk Operations")
        print("5. ℹ️  System Information")
        print("6. 🚪 Exit")
    
    def _migration_menu(self):
        """Migration operations menu."""
        print(f"\n🚀 Migration Operations")
        print("=" * 30)
        print("1. 📊 Analyze Current Structure")
        print("2. 📝 Generate Registry from Current Files")
        print("3. 🔄 Perform Full Migration to ID-Based System")
        print("4. ↩️  Rollback Migration")
        print("5. 📜 Update JavaScript Files")
        print("6. ⬅️  Back to Main Menu")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == '1':
            self.migrator.analyze_current_structure()
        elif choice == '2':
            if self.migrator.create_backup():
                self.migrator.generate_registry_from_current()
            else:
                print("❌ Could not create backup. Aborting.")
        elif choice == '3':
            self._perform_full_migration()
        elif choice == '4':
            self.migrator.rollback_migration()
        elif choice == '5':
            self.js_updater.update_content_loader()
            self.js_updater.update_dynamic_loader()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice!")
    
    def _perform_full_migration(self):
        """Perform full migration with confirmations."""
        print("\n⚠️ FULL MIGRATION WARNING")
        print("=" * 30)
        print("This will:")
        print("- Rename ALL poem files to poem001.md, poem002.md, etc.")
        print("- Rename ALL image files to image001.png, image002.png, etc.")
        print("- Update ALL image references in poem files")
        print("- Update JavaScript files with new paths")
        print("- Delete original files after successful migration")
        
        confirm1 = input("\nType 'I UNDERSTAND' to continue: ").strip()
        if confirm1 != 'I UNDERSTAND':
            print("❌ Migration cancelled.")
            return
        
        # Create backup
        if not self.migrator.create_backup():
            print("❌ Could not create backup. Aborting migration.")
            return
        
        # Final confirmation
        confirm2 = input("Final confirmation - type 'MIGRATE' to proceed: ").strip()
        if confirm2 != 'MIGRATE':
            print("❌ Migration cancelled.")
            return
        
        # Perform migration
        if self.migrator.perform_migration():
            print("\n🎉 Migration completed!")
            
            # Update JavaScript files
            print("\nUpdating JavaScript files...")
            self.js_updater.update_content_loader()
            self.js_updater.update_dynamic_loader()
            
            # Final validation
            print("\nPerforming final validation...")
            self.validator.validate_registry_integrity()
            self.validator.test_website_functionality()
            
            print("\n✅ Full migration process completed successfully!")
        else:
            print("\n❌ Migration failed. Use rollback option if needed.")
    
    def _image_management_menu(self):
        """Image management menu."""
        print(f"\n🖼️ Image Management")
        print("=" * 30)
        print("1. 📋 List Unassigned Images")
        print("2. 📝 List Poems Without Images")
        print("3. 🤝 Manual Image Assignment")
        print("4. 🤖 Auto-Suggest Assignments")
        print("5. ⬅️  Back to Main Menu")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == '1':
            unassigned = self.image_manager.list_unassigned_images()
            print(f"\n📊 Found {len(unassigned)} unassigned images:")
            for image_id in unassigned:
                image_data = self.registry.registry["images"][image_id]
                original = image_data.get("original_filename", "unknown")
                print(f"   • {image_id} (was: {original})")
        
        elif choice == '2':
            without_images = self.image_manager.list_poems_without_images()
            print(f"\n📊 Found {len(without_images)} poems without images:")
            for poem_id in without_images:
                poem_data = self.registry.registry["poems"][poem_id]
                title = poem_data.get("title", "Unknown")
                print(f"   • {poem_id}: {title}")
        
        elif choice == '3':
            self.image_manager.manual_image_assignment_interface()
        
        elif choice == '4':
            suggestions = self.image_manager.auto_suggest_image_assignments()
            print(f"\n🤖 Auto-suggestions ({len(suggestions)} found):")
            for poem_id, image_id in suggestions.items():
                poem_title = self.registry.registry["poems"][poem_id].get("title", "Unknown")
                image_original = self.registry.registry["images"][image_id].get("original_filename", "unknown")
                print(f"   • {poem_id} ({poem_title}) → {image_id} (was: {image_original})")
        
        elif choice == '5':
            return
        else:
            print("❌ Invalid choice!")
    
    def _validation_menu(self):
        """Validation and testing menu."""
        print(f"\n🔍 Validation & Testing")
        print("=" * 30)
        print("1. 🔍 Validate Registry Integrity")
        print("2. 🌐 Test Website Functionality")
        print("3. 📊 Generate Full Report")
        print("4. ⬅️  Back to Main Menu")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == '1':
            self.validator.validate_registry_integrity()
        elif choice == '2':
            self.validator.test_website_functionality()
        elif choice == '3':
            self._generate_full_report()
        elif choice == '4':
            return
        else:
            print("❌ Invalid choice!")
    
    def _bulk_operations_menu(self):
        """Bulk operations menu."""
        print(f"\n📦 Bulk Operations")
        print("=" * 30)
        print("1. 📊 Collection Statistics")
        print("2. 🏷️  Bulk Metadata Update")
        print("3. 🔄 Regenerate All IDs")
        print("4. ⬅️  Back to Main Menu")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == '1':
            self._show_collection_statistics()
        elif choice == '2':
            print("🚧 Bulk metadata update coming soon...")
        elif choice == '3':
            print("🚧 ID regeneration coming soon...")
        elif choice == '4':
            return
        else:
            print("❌ Invalid choice!")
    
    def _system_info(self):
        """Show system information."""
        print(f"\nℹ️ System Information")
        print("=" * 30)
        print(f"Registry file: {self.registry.registry_path}")
        print(f"Registry exists: {'✅' if os.path.exists(self.registry.registry_path) else '❌'}")
        print(f"Total poems in registry: {len(self.registry.registry['poems'])}")
        print(f"Total images in registry: {len(self.registry.registry['images'])}")
        
        if self.registry.registry.get("metadata"):
            metadata = self.registry.registry["metadata"]
            print(f"Registry version: {metadata.get('version', 'unknown')}")
            print(f"Created: {metadata.get('created', 'unknown')}")
            print(f"Last updated: {metadata.get('last_updated', 'unknown')}")
    
    def _show_collection_statistics(self):
        """Show detailed collection statistics."""
        print(f"\n📊 Collection Statistics")
        print("=" * 30)
        
        poems = self.registry.registry["poems"]
        images = self.registry.registry["images"]
        
        # Basic counts
        print(f"Total poems: {len(poems)}")
        print(f"Total images: {len(images)}")
        
        # Language breakdown
        languages = {}
        for poem_data in poems.values():
            lang = poem_data.get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
        
        print("\nBy Language:")
        for lang, count in sorted(languages.items()):
            print(f"   {lang}: {count}")
        
        # Form breakdown
        forms = {}
        for poem_data in poems.values():
            form = poem_data.get("form", "unknown")
            forms[form] = forms.get(form, 0) + 1
        
        print("\nBy Form:")
        for form, count in sorted(forms.items()):
            print(f"   {form}: {count}")
        
        # Image assignment status
        poems_with_images = sum(1 for poem_data in poems.values() if poem_data.get("image_id"))
        poems_without_images = len(poems) - poems_with_images
        
        print(f"\nImage Assignment:")
        print(f"   Poems with images: {poems_with_images}")
        print(f"   Poems without images: {poems_without_images}")
        print(f"   Assignment rate: {(poems_with_images/len(poems)*100):.1f}%" if poems else "N/A")
    
    def _generate_full_report(self):
        """Generate comprehensive system report."""
        print(f"\n📋 Full System Report")
        print("=" * 50)
        
        # System info
        self._system_info()
        
        # Statistics
        self._show_collection_statistics()
        
        # Validation
        print(f"\n🔍 Validation Results:")
        issues = self.validator.validate_registry_integrity()
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        print(f"Total validation issues: {total_issues}")
        
        # Website functionality
        print(f"\n🌐 Website Functionality:")
        functionality_ok = self.validator.test_website_functionality()
        print(f"Website ready: {'✅' if functionality_ok else '❌'}")


if __name__ == "__main__":
    cli = PoetryManagerCLI()
    cli.run()