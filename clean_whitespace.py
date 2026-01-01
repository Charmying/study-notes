# 檢查是否所有檔案中內容都沒有只有空白字元的行，若有則將其清除。

# Command Line: python clean_whitespace.py

import os
from pathlib import Path
import re

TEXT_EXTENSIONS = {'.py', '.md', '.txt', '.js', '.ts', '.html', '.css', '.json', '.sample'}

def is_text_file(file_path: Path) -> bool:
    """Quick check if file is likely text by attempting to decode a chunk."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
        chunk.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def clean_whitespace_lines(file_path: Path) -> bool:
    """Clean lines that contain only whitespace."""
    if file_path.suffix not in TEXT_EXTENSIONS or not is_text_file(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines = []
        modified = False

        for line in lines:
            if re.match(r'^\s+$', line):
                cleaned_lines.append('\n')
                modified = True
            else:
                cleaned_lines.append(line)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

    return False

def process_directory(directory: str) -> list[Path]:
    """Process all files in the directory, skipping .git."""
    modified_files = []
    root_path = Path(directory)

    for file_path in root_path.rglob('*'):
        if file_path.is_file() and '.git' not in file_path.parts:
            if clean_whitespace_lines(file_path):
                modified_files.append(file_path)

    return modified_files

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Starting cleanup in directory: {current_dir}")

    modified_files = process_directory(current_dir)

    if modified_files:
        print(f"\nCleaned {len(modified_files)} files:")
        for file_path in sorted(modified_files):
            print(f"  - {file_path}")
    else:
        print("\nNo files needed cleaning")
