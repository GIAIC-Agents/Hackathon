# Implementation Plan: AI Textbook Generator

**Branch**: `001-ai-textbook-spec` | **Date**: 2025-12-06 | **Spec**: /specs/001-ai-textbook-spec/spec.md
**Input**: Feature specification from `/specs/001-ai-textbook-spec/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for the AI Textbook Generator, a Docusaurus-based project that leverages AI for chapter-wise content generation and presents it through a custom React frontend, deployable to GitHub Pages. It covers Docusaurus setup, AI integration strategy, custom UI development, deployment, and validation.

## Technical Context

**Language/Version**: JavaScript (ESNext), Node.js (LTS), React 18+  
**Primary Dependencies**: Docusaurus 3+, React, TailwindCSS (optional, but planned for custom styling), Gemini CLI/Claude Code (for AI generation)  
**Storage**: Local Filesystem (for generated Markdown content and Docusaurus assets)  
**Testing**: Docusaurus build validation, Link checking, potentially Jest/React Testing Library for custom React components.  
**Target Platform**: Web (Static site hosted on GitHub Pages)  
**Project Type**: Web application (Frontend focused, static site generation)  
**Performance Goals**: Fast page load times (achieved via static site generation), efficient Docusaurus build processes.  
**Constraints**: Adherence to Docusaurus Markdown format, GitHub Pages deployment limitations, potential API rate limits for AI generation.  
**Scale/Scope**: Initial project focuses on generating and presenting a single textbook with 3-5 chapters. Designed for extensibility to multiple textbooks and more complex content structures.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   [x] **Structured Content Generation**: Does the plan account for chapter-wise content generation with all required elements (lessons, examples, exercises, summaries)?
*   [x] **Docusaurus-Compatible Markdown**: Is all proposed content generation in Docusaurus-compatible Markdown?
*   [x] **Custom Frontend Development**: Does the plan specify the development of a custom frontend, avoiding the default Docusaurus theme?
*   [x] **Clean and Organized File Structure**: Does the proposed file structure adhere to the `/book/[chapters|components|layouts|docs]` convention?
*   [x] **Spec-Kit Driven Workflow**: Is the plan aligned with the Spec-Kit Plus workflow, with clear inputs and outputs for each stage?
*   [x] **Integrated Toolchain**: Does the plan leverage the integrated toolchain (Spec-Kit, Gemini/Claude, GitHub Pages)?

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-textbook-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
└── contracts/
```

### Source Code (repository root)

```text
book/
├── docusaurus.config.js
├── src/
│   ├── components/      # Custom React components for UI (e.g., Lesson, ChapterCard)
│   ├── theme/           # Docusaurus theme overrides (e.g., Layout, Navbar)
│   └── css/             # Global CSS or TailwindCSS configuration
├── docs/                # Placeholder, or for general Docusaurus docs (not textbook content)
├── chapters/            # AI-generated textbook content (e.g., chapter-1/index.md, chapter-1/lesson-1.md)
├── static/              # Static assets (images, fonts)
├── sidebars.js          # Docusaurus sidebar configuration
└── package.json

.specify/
├── ...

history/
├── ...

# Root level scripts and config
├── README.md
└── package.json         # For root-level scripts or monorepo setup (if applicable)
```

**Structure Decision**: The project will use a dedicated `book/` directory at the repository root for all Docusaurus-related files, adhering to the convention of `/book/[chapters|components|layouts|docs]` for organized content and frontend elements. This structure facilitates clear separation of the generated content from the Docusaurus boilerplate and custom UI components.

### Documentation (this feature)

```text
specs/001-ai-textbook-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
└── contracts/
```

### Source Code (repository root)

```text
book/
├── docusaurus.config.js
├── src/
│   ├── components/      # Custom React components for UI (e.g., Lesson, ChapterCard)
│   ├── theme/           # Docusaurus theme overrides (e.g., Layout, Navbar)
│   └── css/             # Global CSS or TailwindCSS configuration
├── docs/                # Placeholder, or for general Docusaurus docs (not textbook content)
├── chapters/            # AI-generated textbook content (e.g., chapter-1/index.md, chapter-1/lesson-1.md)
├── static/              # Static assets (images, fonts)
├── sidebars.js          # Docusaurus sidebar configuration
└── package.json

.specify/
├── ...

history/
├── ...

# Root level scripts and config
├── README.md
└── package.json         # For root-level scripts or monorepo setup (if applicable)
```

**Structure Decision**: The project will use a dedicated `book/` directory at the repository root for all Docusaurus-related files, adhering to the convention of `/book/[chapters|components|layouts|docs]` for organized content and frontend elements. This structure facilitates clear separation of the generated content from the Docusaurus boilerplate and custom UI components.

## Project Setup Plan

**Goal**: Initialize Docusaurus project and set up basic environment for custom development.

1.  **Initialize Docusaurus Project**:
    *   Run `npx create-docusaurus@latest book classic` to create a new Docusaurus project in the `book/` directory.
    *   Clean up default Docusaurus content (e.g., `docs/` folder, default pages in `src/pages`).

2.  **Directory Creation**:
    *   Create `book/chapters/` for AI-generated Markdown content.
    *   Create `book/src/components/` for custom React components.
    *   Create `book/src/theme/` for Docusaurus theme overrides.
    *   Create `book/src/css/` for global CSS or TailwindCSS setup.

3.  **Install UI Libraries (Optional TailwindCSS)**:
    *   If using TailwindCSS: Install `tailwindcss`, `postcss`, `autoprefixer` within the `book/` directory.
    *   Configure `tailwind.config.js` and `postcss.config.js`.
    *   Integrate TailwindCSS into `book/src/css/custom.css`.

## AI Book Generation Plan

**Goal**: Establish a repeatable process for generating structured textbook chapters using AI, storing them in the correct Docusaurus format.

1.  **AI Tool Selection**: Utilize Gemini CLI or Claude Code as the primary AI content generation tool.

2.  **Chapter Generation Strategy**:
    *   Each chapter will be generated individually using a specific prompt.
    *   A main prompt will define the overall book topic and structure (e.g., "Generate a chapter outline for 'Introduction to AI'").
    *   Sub-prompts will be used for each lesson, example, and exercise within a chapter (e.g., "Generate content for 'Lesson 1.1: What is AI?' for the 'Introduction to AI' chapter, including headings, an example, and 2 exercises.").

3.  **Prompt Reusability**:
    *   Standardized prompt templates will be created to ensure consistent output format (Markdown).
    *   Placeholders within templates will allow dynamic insertion of chapter titles, lesson topics, etc.

4.  **Storage and Naming Convention**:
    *   Generated Markdown files for chapters will be stored in `book/chapters/<chapter-slug>/index.md`.
    *   Generated Markdown files for lessons will be stored in `book/chapters/<chapter-slug>/<lesson-slug>.md`.
    *   `sidebar.js` will be dynamically updated or manually configured to include the new chapters and lessons.

## Frontend Plan

**Goal**: Develop a fully custom Docusaurus frontend, overriding default styles and implementing intuitive navigation.

1.  **Override Default Theme**:
    *   Use Docusaurus "swizzle" command to eject and customize core theme components (e.g., `Layout`, `Navbar`, `DocItem`).
    *   Modify `docusaurus.config.js` to point to the custom theme components.

2.  **Custom Layout Components**:
    *   Create `book/src/theme/Layout/index.js` to define the overall page structure, incorporating custom header, footer, and content area.
    *   Develop `book/src/theme/DocItem/index.js` to control the rendering of individual lesson and chapter pages, ensuring proper display of generated content.

3.  **Typography System**:
    *   Define a consistent typography scale using CSS variables or TailwindCSS classes.
    *   Implement font families, sizes, weights, and line heights for headings, body text, code blocks, and other elements in `book/src/css/custom.css`.

4.  **Chapter Navigation UI**:
    *   Develop custom React components for chapter navigation (e.g., a "Table of Contents" component that dynamically renders based on `sidebar.js`).
    *   Implement "Next/Previous Lesson" buttons within `DocItem` to facilitate sequential reading.
    *   Ensure navigation is responsive and user-friendly.

5.  **Styling (TailwindCSS/CSS)**:
    *   Apply custom styles across all components using TailwindCSS utility classes where possible.
    *   For more complex or global styles, use standard CSS in `book/src/css/custom.css`.
    *   Focus on a clean, academic, and visually appealing design as per the user's initial goal.

## Deployment Plan

**Goal**: Configure the Docusaurus project for deployment to GitHub Pages.

1.  **GitHub Repository Setup**:
    *   Ensure the project is hosted in a GitHub repository.
    *   The `book/` directory should be part of this repository.

2.  **GitHub Pages Configuration**:
    *   Configure GitHub Pages to build from the `gh-pages` branch or directly from the `build` directory (if using GitHub Actions).
    *   Update `docusaurus.config.js` with `baseUrl` and `projectName` properties to correctly serve assets from GitHub Pages.

3.  **`docusaurus.config.js` Changes**:
    *   Set `baseUrl: '/<your-repo-name>/'` (e.g., `'/ai-textbook-generator/'`).
    *   Set `projectName: '<your-repo-name>'`.
    *   Consider setting `organizationName: '<your-github-username-or-org>'` for user/org pages.
    *   Configure the build output directory if deviating from default (`build`).

## Validation Plan

**Goal**: Verify the functionality, content rendering, and build integrity of the AI Textbook Generator.

1.  **Content Rendering Verification**:
    *   Manually review generated chapters and lessons in the Docusaurus development server (`npm start`).
    *   Check for correct Markdown parsing: headings, lists, code blocks, tables, examples, exercises.
    *   Ensure custom React components (if any) used within Markdown render correctly.

2.  **Sidebar and Navigation Verification**:
    *   Confirm that `sidebars.js` correctly loads all generated chapters and lessons.
    *   Verify that clicking on sidebar items navigates to the correct content.
    *   Test "Next/Previous Lesson" buttons for accurate navigation flow.
    *   Ensure responsive behavior of navigation on different screen sizes.

3.  **Build Success and Link Checking**:
    *   Run `npm run build` and ensure the build completes without errors.
    *   Deploy the built site locally or to a staging environment (e.g., using `serve -s build`) to verify production readiness.
    *   Utilize Docusaurus's built-in link checker (if available) or external tools to ensure all internal and external links are valid.

4.  **AI Generation Output Validation**:
    *   Post-generation, review a sample of AI-generated content for adherence to structured format, quality, and relevance to the prompt.
    *   Ensure generated files are placed in the correct `book/chapters/` directory structure.
