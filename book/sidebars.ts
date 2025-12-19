import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar structure for the AI Humanoid Robots book
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 01: Foundations',
      items: [
        'Module-01/Chapter 01 Foundations', // Using the actual filename
        'Module-01/lesson-2',
        'Module-01/lesson-3',
        'Module-01/lesson-4',
        'Module-01/lesson-5',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 02: Core Concepts',
      items: [
        'Module-02/index',
        'Module-02/lesson-6',
        'Module-02/lesson-7',
        'Module-02/lesson-8',
        'Module-02/lesson-9',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 03: Advanced Topics',
      items: [
        'Module-03/index',
        'Module-03/lesson-10',
        'Module-03/lesson-11',
        'Module-03/lesson-12',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 04: Implementation',
      items: [
        'Module-04/index',
        'Module-04/lesson-13',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Extras',
      items: [
        'tutorial-extras/manage-docs-versions',
        'tutorial-extras/translate-your-site',
      ],
      collapsed: true,
    },
  ],
};

export default sidebars;
