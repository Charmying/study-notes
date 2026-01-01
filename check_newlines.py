# 檢查是否所有檔案都以空行結尾

# Command Line: python check_newlines.py

import os

def check_files_ending_with_newline(directory):
    files_without_newline = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.txt', '.py', '.js', '.ts', '.html', '.css', '.json')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        if content and not content.endswith(b'\n') and not content.endswith(b'\r\n'):
                            files_without_newline.append(file_path)
                except Exception as e:
                    print(f"無法讀取檔案 {file_path}: {e}")

    return files_without_newline

# 檢查目錄
directory = r"d:\Code\GitHub\study-note"
files_without_newline = check_files_ending_with_newline(directory)

if files_without_newline:
    print("以下檔案最後沒有空一行：")
    for file_path in files_without_newline:
        print(file_path)
else:
    print("所有檔案都以空行結尾。")
