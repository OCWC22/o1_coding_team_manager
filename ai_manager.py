import json
import os
import asyncio
from openai import OpenAI
import anthropic
from anthropic import AsyncAnthropic

class ProjectManager:
    def __init__(self):
        self.openai_client = OpenAI()
        self.anthropic_client = AsyncAnthropic()
        print("ProjectManager initialized.")

    def generate_project_plan(self, user_input):
        print("Generating project plan based on user input...")
        response = self.openai_client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""As an AI project manager for a team of AI coders, create a detailed plan for a multi-file project based on the following user input: {user_input}

Your response should include:
1. A detailed project plan enclosed in <plan></plan> tags. This plan should outline the overall structure and goals of the project.
2. Instructions for each file in the project, enclosed in <folder/file_name></folder/file_name> tags (or just <file_name></file_name> if the file is in the root folder).

For each file, provide complete and self-sufficient instructions that would allow a human developer to write the file independently, without knowledge of other files in the project. Include details such as:
- The purpose of the file
- Required imports and dependencies
- Functions or classes to be implemented
- How this file interacts with other parts of the project (if applicable) in detail
- Any specific algorithms or logic to be used
- Correct and complete import statements for all required modules and packages
- Detailed instructions on how to structure the file to facilitate imports from and to other files in the project
- All variables, attributes, and classes that need to be defined for each agent
- Ensure that all necessary variables are defined and initialized correctly

Ensure that your instructions for imports and file structure are very clear and precise. This is crucial for the team as they don't know the structure of other files in the project. Specify exactly how each file should be imported and used by other files, including the exact import statements to use.

This project will be built immediately after this plan is generated, so you don't need to mention any kind of scheduling or time-based details, just the specific requirements for each file.
Ensure that your instructions are detailed enough that all files, when developed independently, will work together seamlessly in the final project. Pay special attention to making sure that all imports between files are correctly specified and will work as intended."""
                }
            ]
        )
        print("Project plan generated. Parsing response...")
        print(f".....REASONING TOKENS USED....: {response.usage.completion_tokens_details['reasoning_tokens']}")
        return self._parse_response(response.choices[0].message.content)

    def _parse_response(self, content):
        print("Parsing AI response...")
        plan_start = content.find("<plan>")
        plan_end = content.find("</plan>")
        project_plan = content[plan_start:plan_end + 7] if plan_start != -1 and plan_end != -1 else ""

        file_instructions = {}
        start = 0
        while True:
            file_start = content.find("<", start)
            if file_start == -1:
                break
            file_end = content.find(">", file_start)
            file_name = content[file_start + 1:file_end]
            content_start = file_end + 1
            content_end = content.find(f"</{file_name}>", content_start)
            if content_end == -1:
                break
            file_instructions[file_name] = content[content_start:content_end].strip()
            start = content_end + len(file_name) + 3

        print(f"Parsed {len(file_instructions)} file instructions.")
        return {
            "project_plan": project_plan,
            "file_instructions": file_instructions
        }

    def save_project_details(self, project_details):
        print("Saving project details...")
        if not os.path.exists("project_plan"):
            os.makedirs("project_plan")
            print("Created 'project_plan' folder.")

        with open("project_plan/project_plan.txt", "w") as f:
            f.write(project_details["project_plan"])
        print("Saved project plan to 'project_plan/project_plan.txt'")

        for file_name, instructions in project_details["file_instructions"].items():
            file_path = os.path.join("project_plan", f"{file_name.replace('/', '_')}_instructions.txt")
            with open(file_path, "w") as f:
                f.write(instructions)
            print(f"Saved instructions for '{file_name}' to '{file_path}'")

        print("\nProject plan and file instructions have been saved to the 'project_plan' folder:")
        print("- Project plan: project_plan/project_plan.txt")
        for file_name in project_details["file_instructions"].keys():
            print(f"- File instructions: project_plan/{file_name.replace('/', '_')}_instructions.txt")

    async def generate_file_code(self, project_plan, file_name, file_instructions):
        print(f"Generating code for {file_name}...")
        prompt = f"""As an AI coder, you are tasked with implementing a specific file for a larger project. Here are the details:

Overall Project Plan:
{project_plan}

File to Implement: {file_name}

Specific Instructions for this File:
{file_instructions}

Please generate the complete code for this file. Your response should be the full, runnable code enclosed in <{file_name}></{file_name}> tags. Ensure that your implementation follows the given instructions and integrates well with the overall project plan."""

        response = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return self._extract_code(response.content[0].text, file_name)

    def _extract_code(self, content, file_name):
        start_tag = f"<{file_name}>"
        end_tag = f"</{file_name}>"
        start = content.find(start_tag)
        end = content.find(end_tag)
        if start != -1 and end != -1:
            return content[start + len(start_tag):end].strip()
        else:
            print(f"Warning: Could not extract code for {file_name}")
            return ""

    def save_file_code(self, file_name, code):
        folder_path = os.path.dirname(file_name)
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")

        with open(file_name, "w") as f:
            f.write(code)
        print(f"Saved code to {file_name}")

    async def generate_and_save_project_files(self, project_details):
        print("Generating and saving project files...")
        tasks = []
        for file_name, instructions in project_details["file_instructions"].items():
            task = self.generate_file_code(project_details["project_plan"], file_name, instructions)
            tasks.append(task)
        
        generated_codes = await asyncio.gather(*tasks)
        
        for file_name, code in zip(project_details["file_instructions"].keys(), generated_codes):
            self.save_file_code(file_name, code)

async def main():
    print("Starting project generation process...")
    manager = ProjectManager()
    user_input = input("Please describe the project you want to create: ")
    print(f"User input received: '{user_input}'")
    
    project_details = manager.generate_project_plan(user_input)
    print("Project plan generated successfully.")

    manager.save_project_details(project_details)
    print("Project plan and instructions saved.")

    await manager.generate_and_save_project_files(project_details)
    print("Project files generated and saved.")
    print("Project generation process completed.")

if __name__ == "__main__":
    asyncio.run(main())




