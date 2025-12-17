#!/bin/bash

# This script generates a complete textbook with 4 modules and 13 lessons

# Set up paths
BOOK_DIR="../book/book"
CHAPTERS_DIR="$BOOK_DIR/chapters"
SCRIPTS_DIR="$(dirname "$0")"

# Create chapters directory if it doesn't exist
mkdir -p "$CHAPTERS_DIR"

# Define chapter and lesson counts
MODULE_COUNT=4
LESSONS_PER_MODULE=(3 4 3 3) # Total 13 lessons across 4 modules

# Generate each module (chapter)
for module in {1..4}; do
    echo "Generating Module $module..."
    
    # Create module directory
    MODULE_DIR="$CHAPTERS_DIR/module-$module"
    mkdir -p "$MODULE_DIR"
    
    # Generate chapter overview
    echo "  Generating chapter overview..."
    CHAPTER_PROMPT="$(cat "$SCRIPTS_DIR/chapter-prompt-template.txt" | sed "s/{CHAPTER_TITLE}/Module $module Overview/g" | sed "s/{MODULE_NUMBER}/$module/g" | sed "s/{LESSONS}/Lesson $(($module * 3 - 2)) to Lesson $(($module * 3)) or appropriate range/g" | sed "s/{CORE_TOPICS}/Topics covered in this module/g")"
    
    # Use Gemini CLI to generate chapter content
    # Note: You'll need to replace this with the actual Gemini CLI command
    # For now, we'll create a placeholder file
    echo "# Module $module Overview" > "$MODULE_DIR/index.md"
    echo "" >> "$MODULE_DIR/index.md"
    echo "This is the overview for Module $module." >> "$MODULE_DIR/index.md"
    echo "It covers the following topics:" >> "$MODULE_DIR/index.md"
    echo "" >> "$MODULE_DIR/index.md"
    
    # Generate lessons for this module
    LESSON_COUNT=${LESSONS_PER_MODULE[$((module-1))]} # Array is 0-indexed
    for lesson in $(seq 1 $LESSON_COUNT); do
        echo "  Generating Lesson $lesson for Module $module..."
        
        # Calculate global lesson number (1-13)
        GLOBAL_LESSON_NUM=$(( (module-1) * 3 + lesson ))
        
        # Create lesson content template
        LESSON_PROMPT="$(cat "$SCRIPTS_DIR/lesson-prompt-template.txt" | sed "s/{LESSON_NUMBER}/$GLOBAL_LESSON_NUM/g" | sed "s/{MODULE_NUMBER}/$module/g" | sed "s/{TOPIC}/Topic for Lesson $GLOBAL_LESSON_NUM/g" | sed "s/{CHAPTER_TITLE}/Module $module Overview/g")"
        
        # Use Gemini CLI to generate lesson content
        # Note: You'll need to replace this with the actual Gemini CLI command
        # For now, we'll create a placeholder file
        echo "# Lesson $GLOBAL_LESSON_NUM: Topic for Lesson $GLOBAL_LESSON_NUM" > "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "This is Lesson $GLOBAL_LESSON_NUM from Module $module." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Introduction" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Brief introduction to the topic." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Concepts" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Key concepts covered in this lesson." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Technical Deep Dive" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Technical details and implementation notes." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Diagrams" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Placeholder for diagrams." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Code Examples" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "```python" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "# Example code for Lesson $GLOBAL_LESSON_NUM" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "print('Hello from Lesson $GLOBAL_LESSON_NUM')" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "```" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Exercises" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "1. Exercise 1 for Lesson $GLOBAL_LESSON_NUM" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "2. Exercise 2 for Lesson $GLOBAL_LESSON_NUM" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Quiz" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Q1: Question for Lesson $GLOBAL_LESSON_NUM?" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "A1: Answer for Question 1" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Summary" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "Summary of key points from Lesson $GLOBAL_LESSON_NUM." >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "## Key Terms" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "- Term 1: Definition for Term 1" >> "$MODULE_DIR/lesson-$lesson.md"
        echo "- Term 2: Definition for Term 2" >> "$MODULE_DIR/lesson-$lesson.md"
    done
    
    echo "Module $module generation complete."
    echo ""
done

echo "Textbook generation complete!"
echo "All 4 modules and 13 lessons have been generated."