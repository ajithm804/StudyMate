"""
Script to verify the complete StudyMate project structure
"""
import os
from pathlib import Path

def count_files_and_folders(base_path):
    """Count all files and folders recursively"""
    file_count = 0
    folder_count = 0
    
    for root, dirs, files in os.walk(base_path):
        # Exclude virtual environment and node_modules
        dirs[:] = [d for d in dirs if d not in ['.venv', 'node_modules', '__pycache__', '.git', 'dist', 'build']]
        
        folder_count += len(dirs)
        file_count += len(files)
    
    return file_count, folder_count

def display_tree_structure(base_path, prefix="", is_last=True, max_depth=None, current_depth=0):
    """Display directory tree structure"""
    if max_depth is not None and current_depth >= max_depth:
        return
    
    path = Path(base_path)
    
    # Skip certain directories
    skip_dirs = {'.venv', 'node_modules', '__pycache__', '.git', 'dist', 'build', '.next'}
    
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    items = [item for item in items if item.name not in skip_dirs]
    
    for index, item in enumerate(items):
        is_last_item = index == len(items) - 1
        
        connector = "└── " if is_last_item else "├── "
        print(f"{prefix}{connector}{item.name}")
        
        if item.is_dir():
            extension = "    " if is_last_item else "│   "
            display_tree_structure(
                item, 
                prefix + extension, 
                is_last_item,
                max_depth,
                current_depth + 1
            )

def list_all_files_by_category(base_path):
    """List all files categorized by type"""
    categories = {
        'Python': [],
        'JavaScript/JSX': [],
        'JSON': [],
        'CSS': [],
        'Markdown': [],
        'Config': [],
        'Other': []
    }
    
    for root, dirs, files in os.walk(base_path):
        # Exclude certain directories
        dirs[:] = [d for d in dirs if d not in ['.venv', 'node_modules', '__pycache__', '.git', 'dist', 'build']]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)
            
            if file.endswith('.py'):
                categories['Python'].append(rel_path)
            elif file.endswith(('.js', '.jsx')):
                categories['JavaScript/JSX'].append(rel_path)
            elif file.endswith('.json'):
                categories['JSON'].append(rel_path)
            elif file.endswith('.css'):
                categories['CSS'].append(rel_path)
            elif file.endswith('.md'):
                categories['Markdown'].append(rel_path)
            elif file.endswith(('.txt', '.env', '.gitignore', '.gitkeep')):
                categories['Config'].append(rel_path)
            else:
                categories['Other'].append(rel_path)
    
    return categories

def main():
    """Main function to check project structure"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("="*80)
    print("STUDYMATE PROJECT STRUCTURE VERIFICATION")
    print("="*80)
    print(f"\nProject Root: {base_dir}\n")
    
    # Count files and folders
    file_count, folder_count = count_files_and_folders(base_dir)
    
    print(f"📊 SUMMARY:")
    print(f"   Total Folders: {folder_count}")
    print(f"   Total Files: {file_count}")
    print(f"   Total Items: {file_count + folder_count}")
    
    print("\n" + "="*80)
    print("📁 DIRECTORY TREE STRUCTURE")
    print("="*80 + "\n")
    
    print("StudyMate1/")
    display_tree_structure(base_dir, prefix="", max_depth=4)
    
    print("\n" + "="*80)
    print("📄 FILES BY CATEGORY")
    print("="*80 + "\n")
    
    categories = list_all_files_by_category(base_dir)
    
    total_files = 0
    for category, files in categories.items():
        if files:
            print(f"\n{category} Files ({len(files)}):")
            print("-" * 40)
            for file in sorted(files):
                print(f"  • {file}")
            total_files += len(files)
    
    print("\n" + "="*80)
    print("✅ VERIFICATION COMPLETE")
    print("="*80)
    print(f"\nTotal Files Analyzed: {total_files}")
    
    # Check for critical files
    print("\n" + "="*80)
    print("🔍 CRITICAL FILES CHECK")
    print("="*80 + "\n")
    
    critical_files = [
        'README.md',
        '.gitignore',
        'ai_service/app.py',
        'ai_service/requirements.txt',
        'backend/server.js',
        'backend/package.json',
        'frontend/package.json',
        'frontend/vite.config.js',
        'scripts/ingest_pdfs.py',
        'scripts/rebuild_embeddings.py'
    ]
    
    for file in critical_files:
        file_path = os.path.join(base_dir, file)
        status = "✅" if os.path.exists(file_path) else "❌ MISSING"
        print(f"{status} {file}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
