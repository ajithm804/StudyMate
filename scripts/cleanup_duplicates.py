"""
Script to clean up duplicate folders and organize the project structure
"""
import os
import shutil

def cleanup_duplicates():
    """Remove duplicate folders and consolidate structure"""
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("="*80)
    print("🧹 STUDYMATE PROJECT CLEANUP")
    print("="*80)
    
    # Folders to remove (duplicates)
    remove_folders = [
        'backend/server',
        'frontend/client', 
        'flask_service'
    ]
    
    print("\n📋 The following duplicate folders will be REMOVED:")
    for folder in remove_folders:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            print(f"   ❌ {folder}")
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will permanently delete the above folders!")
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Cleanup cancelled.")
        return
    
    print("\n🗑️  Removing duplicate folders...")
    
    for folder in remove_folders:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"   ✅ Removed: {folder}")
            except Exception as e:
                print(f"   ❌ Error removing {folder}: {e}")
    
    print("\n" + "="*80)
    print("✅ CLEANUP COMPLETE!")
    print("="*80)
    print("\nYour project structure is now cleaner and organized.")
    print("\nRecommended next steps:")
    print("1. Run: python scripts/check_structure.py")
    print("2. Verify all services work correctly")

if __name__ == "__main__":
    cleanup_duplicates()
