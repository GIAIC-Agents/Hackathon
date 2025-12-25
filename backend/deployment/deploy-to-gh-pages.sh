#!/bin/bash

# This script automates the deployment of the Docusaurus site to GitHub Pages

# Navigate to the book directory
cd book/book

# Build the site
npm run build

# Deploy to GitHub Pages
npm run deploy

echo "Deployment completed successfully!"