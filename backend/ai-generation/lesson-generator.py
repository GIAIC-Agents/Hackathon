import subprocess
import sys
import os

def generate_lesson(chapter_id, lesson_id, topic, chapter_context):
    """
    Generate a lesson using Gemini CLI based on a template.
    
    Args:
        chapter_id (str): The chapter ID (e.g., 'module-1')
        lesson_id (str): The lesson ID (e.g., 'lesson-1')
        topic (str): The topic of the lesson
        chapter_context (str): Context from the chapter overview
    """
    # Read the lesson prompt template
    with open('chapter-prompt-template.txt', 'r') as f:
        template = f.read()
    
    # Replace placeholders in the template
    prompt = template.replace('{CHAPTER_ID}', chapter_id)
    prompt = prompt.replace('{LESSON_ID}', lesson_id)
    prompt = prompt.replace('{TOPIC}', topic)
    prompt = prompt.replace('{CHAPTER_CONTEXT}', chapter_context)
    
    # Create directory for this chapter if it doesn't exist
    chapter_dir = f'book/chapters/{chapter_id}'
    os.makedirs(chapter_dir, exist_ok=True)
    
    # Generate lesson content using Gemini CLI
    try:
        result = subprocess.run([
            'gemini',
            'generate',
            '--prompt',
            prompt,
            '--output-format',
            'markdown'
        ], capture_output=True, text=True, check=True)
        
        # Save the generated content to a file
        lesson_file = f'{chapter_dir}/{lesson_id}.md'
        with open(lesson_file, 'w') as f:
            f.write(result.stdout)
            
        print(f'Successfully generated {lesson_file}')
        return True
        
    except subprocess.CalledProcessError as e:
        print(f'Error generating lesson: {e}')
        return False

def main():
    if len(sys.argv) != 5:
        print("Usage: python lesson-generator.py <chapter_id> <lesson_id> <topic> <chapter_context>")
        sys.exit(1)
    
    chapter_id = sys.argv[1]
    lesson_id = sys.argv[2]
    topic = sys.argv[3]
    chapter_context = sys.argv[4]
    
    success = generate_lesson(chapter_id, lesson_id, topic, chapter_context)
    if not success:
        sys.exit(1)

def regenerate_lesson(chapter_id, lesson_id):
    """
    Regenerate a specific lesson based on its ID.
    """
    # Read the existing lesson file to get topic and context
    lesson_file = f'book/chapters/{chapter_id}/{lesson_id}.md'
    try:
        with open(lesson_file, 'r') as f:
            content = f.read()
        
        # Extract topic from the lesson content (simplified - in practice, you'd need more sophisticated parsing)
        topic = ""  # This would need to be extracted from the MD content
        chapter_context = ""  # This would need to be retrieved from the chapter overview
        
        # Generate the lesson again
        success = generate_lesson(chapter_id, lesson_id, topic, chapter_context)
        return success
        
    except FileNotFoundError:
        print(f'Lesson file {lesson_file} not found')
        return False

if __name__ == '__main__':
    main()