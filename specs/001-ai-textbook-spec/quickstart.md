# Quickstart: AI Textbook Generator Frontend

This guide provides instructions to quickly set up and run the Docusaurus frontend for the AI Textbook Generator.

## Prerequisites

-   Node.js (LTS version recommended)
-   npm or Yarn
-   Git

## 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone [REPOSITORY_URL]
cd [PROJECT_DIRECTORY]
```

## 2. Install Dependencies

Navigate to the `book/` directory (where your Docusaurus project will reside) and install the necessary Node.js packages:

```bash
cd book
npm install   # or yarn install
```

## 3. Start the Development Server

Once dependencies are installed, you can start the Docusaurus development server to preview your site:

```bash
npm start     # or yarn start
```

This will open a new browser window at `http://localhost:3000` (or another available port). Any changes you make to the Markdown content or React components will be reflected automatically.

## 4. Build for Production

To create a production-ready static build of your Docusaurus site, run:

```bash
npm run build   # or yarn build
```

The static assets will be generated in the `build/` directory within your `book/` folder. These files can then be deployed to any static hosting service, such as GitHub Pages.

## 5. Generate Textbook Content (Conceptual - AI Tooling)

*(Note: This section describes the conceptual steps for generating content using AI tools. The actual commands will be defined in the Automation Specification and executed via Spec-Kit Plus.)*

To generate or update the textbook content, you would typically use specific Spec-Kit commands that invoke the Gemini CLI or Claude Code. For example:

```bash
# Example: Generate a new chapter
/sp.generate-chapter "Introduction to AI"

# Example: Update an existing lesson
/sp.update-lesson "Chapter 1, Lesson 3: Neural Networks"
```

These commands would place the generated Markdown files into the `/book/chapters/` directory, which Docusaurus will then pick up.