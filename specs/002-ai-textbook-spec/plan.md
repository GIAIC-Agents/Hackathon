# Implementation Plan: AI Textbook Specification

**Branch**: `002-ai-textbook-spec` | **Date**: Sunday, December 7, 2025 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/002-ai-textbook-spec/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for an AI Textbook Generator that creates a Docusaurus-based textbook from a course outline. The technical approach involves using Docusaurus for the frontend, integrating custom React components with Tailwind CSS for styling, and defining a Gemini CLI-based AI generation flow for content. The generated textbook will feature a structured book layout with chapters, lessons, and a defined pedagogical format, ready for deployment to GitHub Pages.

## Technical Context

**Language/Version**: JavaScript (Node.js for Docusaurus, React), Python (for AI generation scripts/ROS 2 examples)  
**Primary Dependencies**: Docusaurus, React, Tailwind CSS, Gemini CLI  
**Storage**: N/A (static site generation, content stored as Markdown files)  
**Testing**: Docusaurus built-in testing (if applicable), manual content review, UI testing  
**Target Platform**: Web (Docusaurus static site)  
**Project Type**: Web application (static site generator)  
**Performance Goals**: Generated textbook builds in under 30 minutes. Docusaurus site loads efficiently on modern browsers.  
**Constraints**: AI generation token limits for lesson/chapter content. GitHub Pages deployment limitations.  
**Scale/Scope**: 4 chapters, 13 lessons, single textbook generation instance.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle 1: Library-First**: The AI generation logic for lessons/chapters should be encapsulated in a reusable manner, potentially as a set of scripts or functions that can be invoked modularly.
**Principle 2: CLI Interface**: The AI generation flow is explicitly designed to be driven by the Gemini CLI, adhering to text in/out protocols.
**Principle 3: Test-First (NON-NEGOTIABLE)**: Tests will be defined for Docusaurus component rendering, navigation, and the overall build/deployment pipeline, as well as validation of AI-generated content structure.
**Principle 4: Integration Testing**: Integration tests will focus on the end-to-end generation process, Docusaurus build, and deployment to ensure all components work together seamlessly.

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-textbook-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book/
├── src/
│   ├── components/            # Custom React components (Header, Sidebar, ChapterCard, LessonLayout)
│   ├── css/                   # Tailwind CSS configuration
│   └── theme/                 # Custom Docusaurus theme overrides
├── chapters/                  # Generated Markdown for book chapters and lessons
│   ├── module-1/
│   │   ├── lesson-1.md
│   │   └── ...
│   └── module-2/
│       └── ...
├── static/                    # Static assets (diagrams, images)
├── docusaurus.config.js       # Docusaurus configuration
├── sidebars.js                # Generated sidebar navigation
└── package.json               # Docusaurus project dependencies

scripts/
├── ai-generation/             # Python/Node.js scripts for AI content generation
│   ├── lesson-generator.py
│   ├── chapter-generator.py
│   └── full-book-generator.sh
├── deployment/                # Scripts for GitHub Pages deployment
└── utils/                     # Helper utilities for content processing

tests/
├── unit/                      # Unit tests for custom React components, utility functions
├── integration/               # Tests for AI generation flow, Docusaurus build/deploy
└── e2e/                       # End-to-end tests for rendered site navigation

```

**Structure Decision**: A monorepo-like structure is chosen with `book/` containing the Docusaurus project and `scripts/` containing the AI generation and deployment logic. This separation allows independent development and testing of the generation logic and the Docusaurus site. `tests/` will house all testing artifacts.

## A. Project Setup Plan

1.  **Initialize Docusaurus Project**: Execute `npx create-docusaurus@latest book classic` to create a new Docusaurus project in the `book/` directory.
2.  **Install Tailwind CSS**: Navigate to `book/` and install Tailwind CSS: `npm install -D tailwindcss postcss autoprefixer`. Configure `tailwind.config.js` and `postcss.config.js`.
3.  **Remove Default Theme**: Modify `docusaurus.config.js` to remove references to the default theme and prepare for custom theme integration.
4.  **Create Custom Theme Folder**: Create `book/src/theme/` directory for custom Docusaurus theme components and overrides.

## B. Book Generation Plan

1.  **Chapter Generation**: For each of the 4 modules:
    *   Define a chapter-level prompt template (`scripts/ai-generation/chapter-prompt-template.txt`).
    *   Invoke Gemini CLI with the chapter prompt and relevant course outline section to generate chapter overview content.
    *   Store generated chapter content in `book/chapters/module-X/index.md`.
2.  **Lesson Generation**: For each of the 13 lessons (mapped to topics):
    *   Define a lesson-level prompt template (`scripts/ai-generation/lesson-prompt-template.txt`) incorporating pedagogical structure.
    *   Invoke Gemini CLI with the lesson prompt, chapter context, and specific topic to generate lesson content.
    *   Integrate Python/ROS 2 code examples, diagrams, exercises, quiz, summary, and key terms into the generated Markdown.
    *   Store generated lesson content in `book/chapters/module-X/lesson-Y.md`.
3.  **Full Book Generation Sequence**: Orchestrate the chapter and lesson generation using a master script (`scripts/ai-generation/full-book-generator.sh`) that iterates through modules and lessons, managing prompts and output files.

## C. Frontend Plan

1.  **Build Layout Components**: Create custom React components in `book/src/components/`:
    *   `Header.js`: Custom header component.
    *   `Sidebar.js`: Custom sidebar component (replacing default Docusaurus sidebar). 
    *   `ChapterCard.js`: Component for displaying chapter information.
    *   `LessonLayout.js`: Custom layout component for individual lesson pages, incorporating the pedagogical structure.
2.  **Build Custom Theme**: Override default Docusaurus theme components in `book/src/theme/` to apply custom styling and integrate custom components. 
3.  **Build Navigation and Sidebar**: Develop `book/sidebars.js` generation rules to dynamically create navigation links for chapters and lessons based on the generated content structure.
4.  **Add Tailwind Configuration**: Configure `book/tailwind.config.js` to define typography, color palette, and other design tokens. Ensure Tailwind utility classes are integrated into custom components and Docusaurus styling.

## D. Integration Plan

1.  **Add Book Markdown Pages**: Ensure all generated chapter (`index.md`) and lesson (`lesson-Y.md`) Markdown files are placed in the correct `book/chapters/module-X/` directories.
2.  **Import into Sidebar**: Configure `book/sidebars.js` (or a generation script for it) to include all generated chapters and lessons in the Docusaurus navigation structure.
3.  **Link Chapters to Frontend UI**: Ensure `ChapterCard` components (or similar UI elements) on the main page link correctly to the respective chapter introduction pages.

## E. Deployment Plan

1.  **GitHub Repo Setup**: Initialize a Git repository, commit the Docusaurus project, and push to a GitHub repository.
2.  **GitHub Pages Instructions**: Document the steps to enable GitHub Pages for the repository, including branch selection (e.g., `gh-pages` or `main` branch `/docs` folder).
3.  **GitHub Pages Build Commands**: Provide Docusaurus build commands and any necessary pre-deployment scripts (`book/docusaurus.config.js` edits for `baseUrl`, `projectName`, `organizationName`).

## F. Validation Plan

1.  **Test Rendering**: Manually review rendered Docusaurus pages to ensure all custom components, typography, and Tailwind styles are applied correctly.
2.  **Test Navigation**: Verify all sidebar links, chapter links, and internal lesson navigation work as expected.
3.  **Test Build Pipeline**: Run `npm run build` within the `book/` directory to ensure the Docusaurus site builds successfully without errors. Validate the deployment to GitHub Pages by accessing the live URL.
4.  **Content Structure Validation**: Implement a script (or manual checklist) to verify that AI-generated lessons adhere to the pedagogical structure (e.g., presence of Introduction, Concepts, Code Examples, etc.).

## Complexity Tracking

No complexity violations identified at this stage.