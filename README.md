# Project Overview

This project consists of two main Python scripts: `ai_manager.py` and `count_lines.py`.

## ai_manager.py

The `ai_manager.py` script is designed to help generate and manage a project plan for a team of AI coders. It uses the OpenAI and Anthropic APIs to generate detailed project plans and specific instructions for each file in the project. The script can also generate the actual code for each file based on the provided instructions and save the generated code to the appropriate files.

### Key Features:
- **Generate Project Plan**: Takes user input and generates a detailed project plan with specific instructions for each file.
- **Save Project Details**: Saves the project plan and file instructions to the `project_plan` folder.
- **Generate File Code**: Uses the Anthropic API to generate the code for each file based on the instructions.
- **Save File Code**: Saves the generated code to the appropriate files.

### How It Works:
1. **Initialization**: The `ProjectManager` class initializes the OpenAI and Anthropic clients.
2. **Generate Project Plan**: The `generate_project_plan` method takes user input and generates a project plan using the OpenAI API.
3. **Parse Response**: The `_parse_response` method extracts the project plan and file instructions from the AI response.
4. **Save Project Details**: The `save_project_details` method saves the project plan and file instructions to the `project_plan` folder.
5. **Generate and Save Project Files**: The `generate_and_save_project_files` method generates the code for each file and saves it.

## count_lines.py

The `count_lines.py` script is a utility to count the number of lines in Python files within a directory, excluding the `ai_manager.py` file.

### Key Features:
- **Count Lines in File**: The `count_lines` function counts the number of lines in a given file.
- **Count Lines in Directory**: The `count_lines_in_directory` function counts the total number of lines in all Python files within a directory, excluding `ai_manager.py`.

### How It Works:
1. **Count Lines in File**: The `count_lines` function opens a file and counts the number of lines.
2. **Count Lines in Directory**: The `count_lines_in_directory` function traverses the directory, counts the lines in each Python file (excluding `ai_manager.py`), and prints the line count for each file.
3. **Print Total Lines**: The total number of lines in all Python files (excluding `ai_manager.py`) is printed.

## Requirements

To run these scripts, you need to have the following Python packages installed:
- `openai`
- `anthropic`

You can install these packages using the following command:
