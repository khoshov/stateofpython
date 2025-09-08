# Frontend Installation Guide

Due to npm cache issues, here are alternative installation methods:

## Option 1: Use Yarn (Recommended)
```bash
# Install yarn if you don't have it
npm install -g yarn

# Install dependencies
yarn install

# Run the development server
yarn dev
```

## Option 2: Fix npm cache manually
```bash
# Fix npm permissions (requires admin)
sudo chown -R $(whoami) ~/.npm

# Clear cache
npm cache clean --force

# Install dependencies
npm install

# Run the development server
npm run dev
```

## Option 3: Use npx directly
```bash
# Run without installing globally
npx next dev
```

## Option 4: Manual dependency installation
The frontend is designed to work with minimal dependencies. If you continue to have issues, you can:

1. Copy the `src` folder to a fresh Next.js project
2. Use create-next-app to create a new project
3. Replace the generated files with our custom ones

## Current Dependencies
The simplified package.json only includes:
- `react` and `react-dom` - React framework
- `next` - Next.js framework  
- `clsx` and `tailwind-merge` - CSS utilities
- `class-variance-authority` - Component variants

All UI components are built with native HTML elements and Tailwind CSS classes, avoiding external UI library dependencies.