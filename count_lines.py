import os

def count_lines(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file)

def count_lines_in_directory(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py') and filename != 'ai_manager.py':
                file_path = os.path.join(root, filename)
                lines = count_lines(file_path)
                total_lines += lines
                print(f"{file_path}: {lines} lines")
    return total_lines

total_lines = count_lines_in_directory('.')

print(f"\nTotal lines (excluding ai_manager.py): {total_lines}")
