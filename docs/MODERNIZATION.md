# Frontend Modernization

This document outlines the modernization of the Picky frontend, moving from a vanilla JavaScript implementation to a modern React application.

## Why the Change?

The original vanilla JavaScript frontend, while functional, presented several challenges:

*   **Maintainability:** As the application grows, managing the codebase becomes increasingly difficult. The lack of a structured architecture makes it hard to add new features and fix bugs.
*   **Scalability:** The original implementation does not scale well. Adding new features requires significant changes to the existing codebase, increasing the risk of introducing new bugs.
*   **Developer Experience:** The lack of a modern build system and development tools makes the development process slow and inefficient.

## The New Architecture

The new frontend is built with [React](https://reactjs.org/) and [Vite](https://vitejs.dev/). This combination provides a modern, fast, and efficient development experience.

### Key Features

*   **Component-Based Architecture:** The UI is broken down into small, reusable components. This makes the codebase easier to understand, maintain, and test.
*   **State Management:** The application state is managed with React's built-in `useState` and `useEffect` hooks. This provides a clear and predictable way to manage data.
*   **Declarative UI:** React's declarative approach to UI development makes it easier to reason about the application's state and how it maps to the UI.
*   **Modern Build System:** Vite provides a fast and efficient build system with features like hot module replacement (HMR) and tree shaking.

## How to Run the New Frontend

The new frontend is located in the `frontend-react` directory. To run it, you'll need to have [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) installed.

1.  Navigate to the `frontend-react` directory:
    ```bash
    cd frontend-react
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

The development server will be available at `http://localhost:5173`.

## Building for Production

To build the application for production, run the following command:

```bash
npm run build
```

This will create a `dist` directory with the production-ready files. These files can then be served by the Python backend.
