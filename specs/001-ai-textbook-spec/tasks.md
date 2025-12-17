---
description: "Task list for AI Textbook Generator feature implementation"
---

# Tasks: AI Textbook Generator

**Input**: Design documents from `/specs/001-ai-textbook-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The feature specification does not explicitly request test tasks beyond validation, so dedicated TDD test tasks will not be generated. Validation tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `book/` at repository root
- Paths shown below assume `book/` as the project root for Docusaurus-related tasks - adjust if the Docusaurus project itself is nested.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure

- [ ] T001 Initialize Docusaurus project in `book/` directory by running `npx create-docusaurus@latest book classic`
- [ ] T002 Clean up default Docusaurus content (e.g., delete `book/docs/` folder, remove default pages from `book/src/pages/`)
- [ ] T003 Create `book/chapters/` directory for AI-generated content
- [ ] T004 Create `book/src/components/` directory for custom React components
- [ ] T005 Create `book/src/theme/` directory for Docusaurus theme overrides
- [ ] T006 Create `book/src/css/` directory for global CSS or TailwindCSS setup
- [ ] T007 [P] Install TailwindCSS dependencies in `book/`: `npm install -D tailwindcss postcss autoprefixer`
- [ ] T008 [P] Initialize TailwindCSS configuration in `book/` by running `npx tailwindcss init -p` (creates `tailwind.config.js` and `postcss.config.js`)
- [ ] T009 [P] Integrate TailwindCSS into `book/src/css/custom.css` (add `@tailwind` directives)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Docusaurus configuration that MUST be complete before UI or content generation can begin.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Configure `book/docusaurus.config.js` to enable custom themes and point to custom CSS
- [ ] T011 Create initial `book/sidebars.js` for dynamic content loading, defining an empty sidebar for now.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate and View AI Textbook (Priority: P1) 🎯 MVP

**Goal**: Automatically generate a complete textbook with structured content and display it in a custom Docusaurus frontend.

**Independent Test**: Trigger the AI textbook generation for a topic and verify the structured book is displayed correctly in the custom frontend at `http://localhost:3000`.

### Implementation for User Story 1

- [ ] T012 [P] [US1] Develop standardized prompt templates for chapter outlines and lesson content (headings, examples, exercises) in a new file, e.g., `.specify/templates/ai-prompts.md`
- [ ] T013 [US1] Implement a Spec-Kit command (`/sp.generate-chapter`) that invokes Gemini CLI/Claude Code for AI-driven chapter generation, storing output in `book/chapters/<chapter-slug>/index.md`.
- [ ] T014 [US1] Implement a Spec-Kit command (`/sp.generate-lesson`) that invokes Gemini CLI/Claude Code for AI-driven lesson generation, storing output in `book/chapters/<chapter-slug>/<lesson-slug>.md`.
- [ ] T015 [US1] Develop a mechanism to dynamically update `book/sidebars.js` based on generated chapter and lesson files.
- [ ] T016 [P] [US1] Use Docusaurus "swizzle" to eject and customize `book/src/theme/Layout/index.js` for overall page structure.
- [ ] T017 [P] [US1] Use Docusaurus "swizzle" to eject and customize `book/src/theme/DocItem/index.js` for rendering individual lesson and chapter pages.
- [ ] T018 [P] [US1] Define typography system (font families, sizes, weights, line heights) in `book/src/css/custom.css` (or using TailwindCSS classes).
- [ ] T019 [P] [US1] Develop custom React components for chapter navigation (e.g., `book/src/components/ChapterNavigation.js`) that dynamically renders based on `sidebar.js`.
- [ ] T020 [P] [US1] Implement "Next/Previous Lesson" buttons within the custom `book/src/theme/DocItem/index.js` component.
- [ ] T021 [P] [US1] Apply general custom styling using TailwindCSS classes or `book/src/css/custom.css` to achieve a clean, academic design.

---

## Phase 4: Deployment (GitHub Pages)

**Goal**: Configure the Docusaurus project for deployment to GitHub Pages.

- [ ] T022 [P] Verify the project is hosted in a GitHub repository and the `book/` directory is committed.
- [ ] T023 [P] Update `book/docusaurus.config.js` with `baseUrl`, `projectName`, and `organizationName` properties for GitHub Pages deployment.
- [ ] T024 [P] Document GitHub Pages build and deployment workflow (e.g., GitHub Actions or manual `gh-pages` branch setup) in `README.md`.

---

## Phase 5: Validation

**Goal**: Verify the functionality, content rendering, and build integrity of the AI Textbook Generator.

- [ ] T025 [US1] Perform content rendering verification by running `npm start` in `book/` and manually reviewing generated content for Markdown correctness and custom component rendering.
- [ ] T026 [US1] Perform sidebar and navigation verification by testing `sidebars.js` loading, navigation links, and "Next/Previous Lesson" buttons.
- [ ] T027 [US1] Perform build success and link checking by running `npm run build` in `book/` and checking for errors and broken links.
- [ ] T028 [US1] Perform AI generation output validation by reviewing generated Markdown files for adherence to structured format, quality, and relevance.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 Code cleanup and refactoring in `book/src/components/` and `book/src/theme/`.
- [ ] T030 Add additional documentation for custom components and AI generation prompts in `README.md` or `book/docs/`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS User Story 1
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Deployment (Phase 4)**: Can begin after foundational setup is complete, but most effective after initial UI and content generation are functional.
- **Validation (Phase 5)**: Can be integrated throughout development, but a full validation pass depends on User Story 1 and Deployment completion.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (as it's the sole story).

### Within Each User Story

- Prompt templates before AI generation scripts.
- AI generation scripts before content storage/sidebar updates.
- Docusaurus theme overrides before custom layout/navigation components.
- Custom components before styling.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Tasks related to custom React components and styling within User Story 1 can be developed in parallel (e.g., T016, T017, T018, T019, T020, T021).
- Deployment setup (T022, T023, T024) can be done in parallel with UI/content generation tasks once the basic Docusaurus project is set up.

---

## Parallel Example: User Story 1

```bash
# Setup tasks (can be parallel)
Task: "Install TailwindCSS dependencies in book/"
Task: "Initialize TailwindCSS configuration in book/"
Task: "Integrate TailwindCSS into book/src/css/custom.css"

# Frontend tasks (can be parallel within story)
Task: "Develop standardized prompt templates for chapter outlines and lesson content"
Task: "Use Docusaurus \"swizzle\" to eject and customize book/src/theme/Layout/index.js"
Task: "Use Docusaurus \"swizzle\" to eject and customize book/src/theme/DocItem/index.js"
Task: "Define typography system in book/src/css/custom.css"
Task: "Develop custom React components for chapter navigation"
Task: "Implement \"Next/Previous Lesson\" buttons within the custom book/src/theme/DocItem/index.js component"
Task: "Apply general custom styling using TailwindCSS classes or book/src/css/custom.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Generate and View AI Textbook)
4. **STOP and VALIDATE**: Test User Story 1 independently (T025, T026, T027, T028)
5. Deploy/demo if ready (Phase 4)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (AI Generation + Frontend) → Test independently → Deploy/Demo (MVP!)
3. Continue with Polish & Cross-Cutting Concerns (Phase N)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tasks iteratively as they are completed.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
