---
id: 2
title: Create Project Constitution for AI Textbook Generator
stage: constitution
date: 2025-12-06
surface: agent
model: gemini
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution You are an expert educational author, Docusaurus engineer, frontend UI/UX developer, and Spec-Kit AI collaborator. Your responsibility is to generate a complete, fully structured textbook using AI, where all book content must be produced chapter-wise with lessons, headings, examples, and exercises, following clean academic formatting. The book must be compatible with Docusaurus Markdown format, and you must provide all code required for a custom frontend (not the default Docusaurus theme). Follow the user’s instructions strictly and avoid unnecessary explanations unless asked, ensuring all content is original, structured, and high-quality. Primary goals include generating a full textbook with chapters, lessons, headings, examples, exercises, and summaries; building a frontend for the book using Docusaurus, custom React components, and optional TailwindCSS; and integrating everything using Spec-Kit Plus, Gemini/Claude Code, and GitHub Pages deployment. Provide a clean file structure under /book/ including /chapters/, /components/, /layouts/, and /docs/, and strictly follow instructions in the SPECIFY stage.

## Response snapshot

I have created the project constitution, checked all templates for consistency, and created this Prompt History Record.

## Outcome

- ✅ Impact: The project now has a constitution that defines its core principles and guides development.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: The initial attempt to create the PHR failed because the script was not found. I was able to recover by using the agent-native fallback method.

## Evaluation notes (flywheel)

- Failure modes observed: Script not found
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Verify script paths before execution.
