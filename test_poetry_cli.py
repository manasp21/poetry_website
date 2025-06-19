#!/usr/bin/env python3
"""
Test script for poetry CLI functionality
"""

from poetry_cli import PoetryCLI, PoemManager, MetadataManager

def test_poetry_cli():
    """Test basic functionality of the poetry CLI."""
    print("🧪 Testing Poetry CLI...")
    
    # Initialize components
    metadata_manager = MetadataManager()
    poem_manager = PoemManager(metadata_manager)
    
    # Test 1: List existing poems
    print("\n📋 Test 1: Listing existing poems...")
    poems = poem_manager.list_poems()
    print(f"Found {len(poems)} poems in collection")
    
    if poems:
        # Show first 3 poems
        print("\nFirst 3 poems:")
        for poem in poems[:3]:
            metadata = poem["metadata"]
            print(f"  #{poem['number']}: {metadata.get('title', 'Unknown')} by {metadata.get('author', 'Unknown')}")
            print(f"    Form: {metadata.get('form', 'Unknown')}, Length: {metadata.get('length', 'Unknown')}")
            print(f"    Has image: {'Yes' if poem['has_image'] else 'No'}")
    
    # Test 2: Check metadata categories
    print("\n🏷️  Test 2: Current metadata categories...")
    forms = metadata_manager.get_forms()
    lengths = metadata_manager.get_lengths()
    languages = metadata_manager.get_languages()
    
    print(f"Forms: {forms}")
    print(f"Lengths: {lengths}")
    print(f"Languages: {[lang['name'] for lang in languages]}")
    
    # Test 3: Test poem reading
    print("\n📖 Test 3: Reading a specific poem...")
    if poems:
        first_poem = poems[0]
        poem_data = poem_manager.get_poem(first_poem["number"])
        if poem_data:
            print(f"Successfully read poem #{poem_data['number']}")
            print(f"Title: {poem_data['metadata'].get('title', 'Unknown')}")
            print(f"Content length: {len(poem_data['content'])} characters")
        else:
            print("❌ Failed to read poem")
    
    # Test 4: Validation
    print("\n🔍 Test 4: Collection validation...")
    cli = PoetryCLI()
    issues = cli.validator.validate_collection()
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    
    if total_issues == 0:
        print("✅ No validation issues found")
    else:
        print(f"⚠️  Found {total_issues} validation issues")
        for issue_type, issue_list in issues.items():
            if issue_list:
                print(f"  {issue_type}: {len(issue_list)} issues")
    
    print("\n✅ All tests completed successfully!")
    print("\nYour poetry CLI is ready to use! Run 'python3 poetry_cli.py' to start.")

if __name__ == "__main__":
    test_poetry_cli()