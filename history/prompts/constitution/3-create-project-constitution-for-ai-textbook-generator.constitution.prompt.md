---
id: 3
title: Create Project Constitution for AI Textbook Generator
stage: constitution
date: 2025-12-06
surface: agent
model: Gemini
feature: none
branch: master
user: 
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:

---

## Prompt

You are an expert educational author, Docusaurus engineer, frontend UI/UX developer, and Spec-Kit AI collaborator. Your responsibility is to generate a complete, fully structured textbook using AI, where all book content must be produced chapter-wise with lessons, headings, examples, and exercises, following clean academic formatting. The book must be compatible with Docusaurus Markdown format, and you must provide all code required for a custom frontend (not the default Docusaurus theme). Follow the user’s instructions strictly and avoid unnecessary explanations unless asked, ensuring all content is original, structured, and high-quality. Primary goals include generating a full textbook with chapters, lessons, headings, examples, exercises, and summaries; building a frontend for the book using Docusaurus, custom React components, and optional TailwindCSS; and integrating everything using Spec-Kit Plus, Gemini/Claude Code, and GitHub Pages deployment. Provide a clean file structure under /book/ including /chapters/, /components/, /layouts/, and /docs/, and strictly follow instructions in the SPECIFY stage.

## Response snapshot

I have successfully created the project constitution and updated the dependent templates. 
- `.specify/memory/constitution.md` was created.
- `.specify/templates/plan-template.md` was updated.
- `.specify/templates/spec-template.md` was updated.
- `.specify/templates/tasks-template.md` was updated.

## Outcome

- ✅ Impact: Created a new project constitution and updated dependent templates.
- 🧪 Tests: n/a
- 📁 Files: 4 files modified
- 🔁 Next prompts: n/a
- 🧠 Reflection: The process of creating a constitution and updating dependent templates is a good way to establish a solid foundation for a project.

## Evaluation notes (flywheel)

- Failure modes observed: n/a
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
