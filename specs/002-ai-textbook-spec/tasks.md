# Tasks: AI Textbook Specification

**Input**: Design documents from `/specs/002-ai-textbook-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The plan.md indicates UI testing, manual content review, and integration tests for build/deploy. Specific test tasks will be integrated where appropriate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown assume the project structure defined in `plan.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure.

- [ ] T001 Initialize Docusaurus project in `book/` using `npx create-docusaurus@latest book classic`
- [ ] T002 Navigate into `book/` directory: `cd book/`
- [ ] T003 [P] Create `scripts/ai-generation/` directory
- [ ] T004 [P] Create `scripts/deployment/` directory
- [ ] T005 [P] Create `scripts/utils/` directory
- [ ] T006 [P] Create `tests/unit/` directory
- [ ] T007 [P] Create `tests/integration/` directory
- [ ] T008 [P] Create `tests/e2e/` directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for Docusaurus theme and styling that MUST be complete before ANY major frontend or content generation work.

**⚠️ CRITICAL**: No user story work depending on custom theming can begin until this phase is complete.

- [ ] T009 Install Tailwind CSS and PostCSS in `book/`: `npm install -D tailwindcss postcss autoprefixer`
- [ ] T010 Configure `book/tailwind.config.js` with basic typography and color palette
- [ ] T011 Configure `book/postcss.config.js`
- [ ] T012 Modify `book/docusaurus.config.js` to remove references to the default theme
- [ ] T013 Create custom theme folder `book/src/theme/`

---

## Phase 3: User Story 1 - Generate Full Textbook (Priority: P1) 🎯 MVP

**Goal**: Generate a complete Docusaurus textbook with 4 chapters and 13 lessons, including pedagogical structure and content.

**Independent Test**: Provide a course outline and verify that a complete, well-structured Docusaurus project is generated, including all specified chapters, lessons, and content elements, ready for local preview.

### Implementation for User Story 1

- [ ] T014 Define chapter-level prompt template in `scripts/ai-generation/chapter-prompt-template.txt`
- [ ] T015 Define lesson-level prompt template in `scripts/ai-generation/lesson-prompt-template.txt` (incorporating pedagogical structure: Intro, Concepts, Technical Deep Dive, Diagrams, Code Examples, Exercises, Quiz, Summary, Key Terms)
- [ ] T016 Implement Python script `scripts/ai-generation/lesson-generator.py` to invoke Gemini CLI and generate individual lesson content based on template
- [ ] T017 Implement Python script `scripts/ai-generation/chapter-generator.py` to invoke Gemini CLI and generate chapter overview content based on template
- [ ] T018 Develop master script `scripts/ai-generation/full-book-generator.sh` to orchestrate chapter and lesson generation for all 4 modules and 13 lessons
- [ ] T019 Create `book/chapters/` directory for generated content
- [ ] T020 [P] Create `book/chapters/module-1/` directory
- [ ] T021 [P] Create `book/chapters/module-2/` directory
- [ ] T022 [P] Create `book/chapters/module-3/` directory
- [ ] T023 [P] Create `book/chapters/module-4/` directory
- [ ] T024 Execute `scripts/ai-generation/full-book-generator.sh` to generate all chapters and lessons, storing Markdown files in respective `book/chapters/module-X/lesson-Y.md` paths.

**Checkpoint**: At this point, the core textbook content should be generated and available as Markdown files in the `book/chapters/` directory.

---

## Phase 4: User Story 2 - Generate Individual Lesson/Chapter (Priority: P2)

**Goal**: Enable users to generate or regenerate specific lessons or chapters independently.

**Independent Test**: Generate a single lesson or chapter within an existing textbook structure and verify its content, structure, and integration into the Docusaurus project without affecting other parts.

### Implementation for User Story 2

- [ ] T025 Enhance `scripts/ai-generation/chapter-generator.py` to accept specific chapter ID/name for regeneration
- [ ] T026 Enhance `scripts/ai-generation/lesson-generator.py` to accept specific lesson ID/name for regeneration
- [ ] T027 Create a CLI interface or a simple script `scripts/ai-generation/regenerate-chapter.sh` to trigger `chapter-generator.py` for a specific chapter
- [ ] T028 Create a CLI interface or a simple script `scripts/ai-generation/regenerate-lesson.sh` to trigger `lesson-generator.py` for a specific lesson

**Checkpoint**: Individual chapter/lesson generation should now be possible.

---

## Phase 5: Frontend Tasks (Cross-Cutting)

**Purpose**: Implement custom Docusaurus frontend components and styling.

- [ ] T029 Create `Header.js` component in `book/src/components/Header.js`
- [ ] T030 Create `Sidebar.js` component in `book/src/components/Sidebar.js`
- [ ] T031 Create `ChapterCard.js` component in `book/src/components/ChapterCard.js`
- [ ] T032 Create `LessonLayout.js` component in `book/src/components/LessonLayout.js`
- [ ] T033 Override Docusaurus theme components in `book/src/theme/` to integrate custom `Header.js` and `Sidebar.js`
- [ ] T034 Integrate `ChapterCard.js` into appropriate Docusaurus page (e.g., `book/src/pages/index.js` for main book overview)
- [ ] T035 Configure `LessonLayout.js` as the default layout for generated lesson Markdown pages
- [ ] T036 Establish typography system using Tailwind classes in `book/tailwind.config.js` and apply to custom components
- [ ] T037 Ensure Tailwind utility classes are integrated and correctly applied across all custom components and theme overrides.

**Checkpoint**: Custom frontend components and styling should be visible when serving the Docusaurus site.

---

## Phase 6: Integration Tasks (Cross-Cutting)

**Purpose**: Link generated content into Docusaurus navigation and verify basic rendering.

- [ ] T038 Implement logic (script or manual edit) to populate `book/sidebars.js` dynamically based on `book/chapters/` directory structure
- [ ] T039 Update `book/docusaurus.config.js` to correctly map `book/chapters/` as content routes
- [ ] T040 Ensure `ChapterCard` components on the homepage link correctly to their respective chapter introduction pages (`book/chapters/module-X/index.md`).

**Checkpoint**: The generated content should be navigable and render correctly within the custom Docusaurus theme.

---

## Phase 7: User Story 3 - Deploy Textbook to GitHub Pages (Priority: P2)

**Goal**: Successfully deploy the generated Docusaurus textbook to GitHub Pages.

**Independent Test**: Successfully deploy a generated Docusaurus project to a GitHub Pages environment and verify that the published site is functional and accessible.

### Implementation for User Story 3

- [ ] T041 Initialize a Git repository in `book/`, commit Docusaurus project files.
- [ ] T042 Create a GitHub repository and push the `book/` project to it.
- [ ] T043 Document clear instructions for enabling GitHub Pages in the repository settings (e.g., selecting `gh-pages` branch or `main` branch `/docs` folder).
- [ ] T044 Provide Docusaurus build command in `book/package.json` scripts: `docusaurus build`
- [ ] T045 Modify `book/docusaurus.config.js` with `baseUrl`, `projectName`, and `organizationName` for GitHub Pages deployment.
- [ ] T046 Create a deployment script `scripts/deployment/deploy-to-gh-pages.sh` to automate Docusaurus build and GitHub Pages deployment.

**Checkpoint**: The textbook should be deployable to GitHub Pages.

---

## Phase 8: Validation & Polish

**Purpose**: Final verification, testing, and cleanup.

- [ ] T047 Run `npm run build` in `book/` and verify successful Docusaurus site build.
- [ ] T048 Serve the Docusaurus site locally (`npm run start` in `book/`) and manually test rendering of all custom components, typography, and Tailwind styles.
- [ ] T049 Manually verify all sidebar links, chapter links, and internal lesson navigation work correctly.
- [ ] T050 Validate the deployment to GitHub Pages by accessing the live URL.
- [ ] T051 Implement a script `tests/integration/validate-content-structure.py` to verify AI-generated lessons adhere to pedagogical structure (e.g., presence of sections like Introduction, Concepts, Code Examples).
- [ ] T052 Refactor and clean up any temporary scripts or unused code.
- [ ] T053 Update `README.md` in `book/` with quickstart instructions and generation/deployment guides.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all major frontend/content generation work.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion and core generation logic from US1.
- **Frontend Tasks (Phase 5)**: Depends on Foundational phase completion. Can run in parallel with US1/US2.
- **Integration Tasks (Phase 6)**: Depends on User Story 1 (for content) and Frontend Tasks (for components).
- **User Story 3 (Phase 7)**: Depends on successful integration and a complete Docusaurus project.
- **Validation & Polish (Phase 8)**: Depends on all other phases being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Requires the core generation logic from US1 to be in place for regeneration features.
- **User Story 3 (P2)**: Requires a working Docusaurus project with generated content and integrated frontend.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- Tasks T003-T008 (directory creation) can run in parallel.
- Tasks T009-T011 (Tailwind setup) can be parallelized with other configuration tasks within Phase 2.
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows).
- All tests for a user story marked [P] can run in parallel.
- Models within a story marked [P] can run in parallel.
- Different user stories can be worked on in parallel by different team members.

---

## Parallel Example: Frontend Components

```bash
# Once Foundational (Phase 2) is complete:
# Developer A:
Task: "Create Header.js component in book/src/components/Header.js"
Task: "Create ChapterCard.js component in book/src/components/ChapterCard.js"

# Developer B:
Task: "Create Sidebar.js component in book/src/components/Sidebar.js"
Task: "Create LessonLayout.js component in book/src/components/LessonLayout.js"

# Once all components are done:
Task: "Override Docusaurus theme components in book/src/theme/ to integrate custom Header.js and Sidebar.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 and Core Frontend)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1 (Full Textbook Generation)
4.  Complete Phase 5: Frontend Tasks (Core UI components for generated content)
5.  Complete Phase 6: Integration Tasks (Linking generated content to UI)
6.  **STOP and VALIDATE**: Test that a full textbook can be generated, and the Docusaurus site renders it correctly with custom UI locally.
7.  Deploy/demo this core functionality if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 (Full Textbook Generation) + Core Frontend + Integration → Test locally → Deploy/Demo (MVP!)
3.  Add User Story 2 (Individual Lesson/Chapter Generation) → Test locally → (Potentially integrate with UI for regen button later)
4.  Add User Story 3 (GitHub Pages Deployment) → Test deployment process → Deploy/Demo
5.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   **Developer A**: Focus on User Story 1 (AI Generation scripts, content storage).
    -   **Developer B**: Focus on Frontend Tasks (React components, custom theme, Tailwind).
    -   **Developer C**: Focus on User Story 2 (Individual generation scripts) and eventually User Story 3 (Deployment).
3.  Integration (Phase 6) would be a shared effort or led by a designated integrator.
4.  Validation (Phase 8) is a team effort.

---

## Notes

-   [P] tasks = different files, minimal dependencies within their phase.
-   [Story] label maps task to specific user story for traceability.
-   Each user story aims to be independently completable and testable.
-   Commit after each task or logical group.
-   Stop at any checkpoint to validate story independently.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
