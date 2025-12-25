import os
import subprocess
import sys
from typing import List, Optional

def generate_chapter(chapter_id: str, chapter_title: str, module_number: int, lessons: List[str], core_topics: List[str]) -> str:
    """
    Generate a chapter using the Gemini CLI with the provided parameters.
    
    Args:
        chapter_id: Unique identifier for the chapter
        chapter_title: Title of the chapter
        module_number: Module number this chapter belongs to
        lessons: List of lesson titles in this chapter
        core_topics: List of core topics covered in this chapter
    
    Returns:
        Generated chapter content as a string
    """
    # Read the chapter prompt template
    with open('chapter-prompt-template.txt', 'r') as f:
        prompt_template = f.read()
    
    # Replace placeholders with actual values
    prompt = prompt_template.format(
        CHAPTER_TITLE=chapter_title,
        MODULE_NUMBER=module_number,
        LESSONS=", ".join(lessons),
        CORE_TOPICS=", ".join(core_topics)
    )
    
    # Write the prompt to a temporary file
    temp_prompt_file = f'temp_prompt_{chapter_id}.txt'
    with open(temp_prompt_file, 'w') as f:
        f.write(prompt)
    
    try:
        # Call Gemini CLI to generate content
        result = subprocess.run([
            'gemini', 'generate', '--prompt-file', temp_prompt_file
        ], capture_output=True, text=True, check=True)
        
        # Return the generated content
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error generating chapter {chapter_id}: {e}")
        return ""
    finally:
        # Clean up temporary file
        if os.path.exists(temp_prompt_file):
            os.remove(temp_prompt_file)

def main():
    """
    Main function to handle command line arguments and generate chapters.
    """
    # Check if we have enough arguments
    if len(sys.argv) < 6:
        print("Usage: python chapter-generator.py <chapter_id> <chapter_title> <module_number> <lesson1,lesson2,...> <topic1,topic2,...>")
        sys.exit(1)
    
    # Parse arguments
    chapter_id = sys.argv[1]
    chapter_title = sys.argv[2]
    module_number = int(sys.argv[3])
    lessons = sys.argv[4].split(',')
    core_topics = sys.argv[5].split(',')
    
    # Generate the chapter
    chapter_content = generate_chapter(chapter_id, chapter_title, module_number, lessons, core_topics)
    
    # Save to file
    output_file = f'../book/chapters/module-{module_number}/index.md'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(chapter_content)
    
    print(f"Chapter {chapter_id} generated successfully!")

if __name__ == "__main__":
    main()