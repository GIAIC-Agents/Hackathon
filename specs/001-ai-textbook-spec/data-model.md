# Data Model: AI Textbook Generator

This project primarily deals with content generation and presentation. The 'data model' here refers to the structure of the textbook content and how it's organized for Docusaurus.

## Entities

### Textbook
Represents the entire book.
-   **Attributes**:
    -   `title`: (string) The title of the textbook.
    -   `description`: (string) A brief overview of the textbook.
    -   `chapters`: (list of Chapter) An ordered list of chapters within the textbook.

### Chapter
Represents a major section of the textbook.
-   **Attributes**:
    -   `id`: (string) Unique identifier (slug for URL).
    -   `title`: (string) The title of the chapter.
    -   `description`: (string, optional) A brief summary of the chapter.
    -   `lessons`: (list of Lesson) An ordered list of lessons within the chapter.
    -   `path`: (string) File path to the chapter's main Markdown file (e.g., `book/chapters/chapter-1/index.md`).

### Lesson
Represents an individual instructional unit within a chapter.
-   **Attributes**:
    -   `id`: (string) Unique identifier (slug for URL).
    -   `title`: (string) The title of the lesson.
    -   `content`: (string) The full Markdown content of the lesson, including headings, examples, and exercises.
    -   `format_headings`: (string) Markdown headings (e.g., `## Introduction`, `### Subtopic`).
    -   `format_examples`: (string) Markdown code blocks or structured text for examples.
    -   `format_exercises`: (string) Markdown lists or structured questions for exercises.
    -   `path`: (string) File path to the lesson's Markdown file (e.g., `book/chapters/chapter-1/lesson-1.md`).

## Relationships

-   `Textbook` 1:N `Chapter` (A textbook contains many chapters)
-   `Chapter` 1:N `Lesson` (A chapter contains many lessons)

## Content Structure (Markdown conventions)

-   Each lesson will be a separate Markdown file.
-   Chapter `index.md` files will serve as the entry point for each chapter and can contain an overview.
-   Headings within lessons should follow standard Markdown (`#`, `##`, `###`, etc.).
-   Examples should be clearly marked, e.g., using code blocks (```python) or a custom admonition (`:::tip Example`).
-   Exercises should be clearly marked, e.g., using a numbered list or a custom admonition (`:::note Exercise`).