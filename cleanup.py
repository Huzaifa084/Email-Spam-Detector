"""
Cleanup script for Email Spam Detection project
This script will identify and optionally remove unnecessary files from the project
"""
import os
import shutil
import argparse

def get_safe_files():
    """Files that should never be deleted"""
    return [
        'main.py',
        'utility.py',
        'README.md',
        'requirements.txt',
        'spam_detection_model.pkl',
        'emails.csv',
        'spam_model_report.json'
    ]

def get_unnecessary_files():
    """Files that can be safely removed"""
    return [
        # Obsolete Python files
        'generate_report.py',  # Functionality moved to utility.py
        'test.py',             # Just a test file
        
        # Jupyter notebooks (development files)
        'Email Spam.ipynb',
        'Email Spam_with_pipeline.ipynb',
        'spam_email_detection_model.ipynb',
        
        # Backup/updated templates (already incorporated)
        'templates/show_updated.html',
        'templates/report_updated.html',
        'templates/index_updated.html',
        
        # Temporary files
        'prediction_count.txt',
        'spam_predictions.txt'
    ]

def cleanup(dry_run=True, specific_file=None):
    """
    Perform the cleanup operation
    
    Args:
        dry_run (bool): If True, only show what would be deleted without actually deleting
        specific_file (str): If provided, only check/remove this specific file
    """
    safe_files = get_safe_files()
    to_remove = get_unnecessary_files() if specific_file is None else [specific_file]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_path in to_remove:
        full_path = os.path.join(base_dir, file_path)
        
        if os.path.exists(full_path):
            if dry_run:
                print(f"Would remove: {file_path}")
            else:
                try:
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    else:
                        os.remove(full_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {str(e)}")
        else:
            print(f"File not found: {file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cleanup unnecessary files from Email Spam Detection project')
    parser.add_argument('--execute', action='store_true', help='Actually remove files (default is dry run)')
    parser.add_argument('--file', type=str, help='Clean up a specific file only')
    
    args = parser.parse_args()
    
    # Run cleanup
    cleanup(dry_run=not args.execute, specific_file=args.file)
    
    if not args.execute:
        print("\nThis was a dry run. No files were actually deleted.")
        print("To remove the files, run with --execute flag.")
