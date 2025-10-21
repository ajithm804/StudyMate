"""
Script to create the complete StudyMate project structure
"""
import os
import sys

def create_directory_structure():
    """Create all necessary directories for the project"""
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    directories = [
        # AI Service
        'ai_service',
        'ai_service/model',
        'ai_service/data',
        'ai_service/data/raw_pdfs',
        'ai_service/data/processed_texts',
        'ai_service/data/vector_store',
        
        # Backend
        'backend',
        'backend/routes',
        'backend/controllers',
        'backend/models',
        'backend/config',
        
        # Frontend
        'frontend',
        'frontend/src',
        'frontend/src/api',
        'frontend/src/components',
        'frontend/src/pages',
        'frontend/src/styles',
        'frontend/public',
        
        # Scripts
        'scripts',
    ]
    
    print("Creating project directory structure...")
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    # Create .gitkeep files
    gitkeep_dirs = [
        'ai_service/data/raw_pdfs',
        'ai_service/data/processed_texts',
        'ai_service/data/vector_store',
    ]
    
    print("\nCreating .gitkeep files...")
    for directory in gitkeep_dirs:
        gitkeep_path = os.path.join(base_dir, directory, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            pass
        print(f"✓ Created: {directory}/.gitkeep")
    
    print("\n" + "="*60)
    print("✅ Project structure created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Navigate to each service directory and install dependencies")
    print("2. Place NCERT PDFs in ai_service/data/raw_pdfs/")
    print("3. Run: python scripts/ingest_pdfs.py")
    print("4. Run: python scripts/rebuild_embeddings.py")
    print("5. Start all services (frontend, backend, ai_service)")

if __name__ == "__main__":
    create_directory_structure()
