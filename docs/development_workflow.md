# Development Workflow

This document outlines the standard development workflow for this project, from idea to deployment. Following this process ensures that our work is tracked, our code is high-quality, and our deployments are consistent.

## Guiding Principles

- **Azure DevOps (ADO)** is the single source of truth for **what** we are building (planning).
- **GitHub** is the single source of truth for **how** we are building it (code).
- **Branching Strategy:** We follow a `feature -> stage -> main` branching model.
  - `main` is our production branch. It should always be stable and deployable.
  - `stage` is our integration and pre-production branch. All feature branches are merged here for testing.
  - `feature/*` branches are for new development and are created from `stage`.
- All work is done on `feature` branches, never directly on `stage` or `main`.
- All code must pass automated checks before being merged into `stage`.
- The only branches that should be created from `main` are the initial `stage` branch and emergency `hotfix/*` branches.

## Current vs Planned State

### Current State
- **Local Development**: Manual execution with `python -m backend.run` or `./run-dev.sh`
- **Testing**: Manual testing via `pytest` command
- **Code Review**: GitHub Copilot PR review configured on GitHub.com (triggers on PR open)
- **No CI/CD**: No GitHub Actions workflows in repository
- **No Deployment**: Local development only

### Planned State
- **Automated CI**: GitHub Actions will run linting and testing on PRs
- **Automated Deployment**: Azure App Service deployment for `stage` and `main` branches
- **Monitoring**: Application Insights and Log Analytics integration

---

## The Workflow: Step-by-Step

### Phase 1: Planning & Setup (in Azure DevOps)

The lifecycle begins when a new idea or requirement is identified.

1.  **Create a Product Backlog Item (PBI):**
    -   **Where:** Azure DevOps (`Boards > Backlogs`)
    -   **What:** Create a new `Product Backlog Item` (PBI).
    -   **Details:** The PBI title should follow the user story format: "As a [user type], I want [to do something] so that [I can achieve some goal]." The description should include acceptance criteria.

2.  **Plan Your Sprint:**
    -   **Where:** Azure DevOps (`Boards > Sprints`)
    -   **What:** During sprint planning, move the PBI from the backlog into the current sprint. This represents a commitment to complete the work.

3.  **Break Down the PBI into Tasks:**
    -   **Where:** Azure DevOps (Inside the PBI)
    -   **What:** Open the PBI and create child `Task` work items for the technical steps required.
    -   **Example Tasks for a PBI:**
        -   `Create new API endpoint in app.py`
        -   `Add delete button to index.html`
        -   `Implement frontend logic in app.js`

4.  **Create a Branch:**
    -   **Where:** Azure DevOps (From the PBI)
    -   **What:** Use the "Create a new branch" feature from the PBI. This will automatically link the branch to the work item. **Base the new branch off `stage`**.

### Phase 2: Development & Committing (Local & GitHub)

Now you move to your local machine to write the code.

1.  **Pull and Check Out the Branch:**
    -   **Where:** Your local terminal.
    -   **What:** Fetch the latest changes from the remote repository and switch to your new feature branch.
    -   **Command:** `git pull && git checkout feature/your-branch-name`

2.  **Write the Code:**
    -   **Where:** Your local editor (e.g., VS Code).
    -   **What:** Implement the code changes required to complete the first `Task`.

3.  **Commit Your Work:**
    -   **Where:** Your local terminal.
    -   **What:** Make small, logical commits. Your commit messages **must** include the Azure DevOps PBI number. This automatically links the commit to the PBI.
    -   **Command:** `git commit -m "Your descriptive message. AB#123"` (replace 123 with your PBI number).

4.  **Push Your Branch:**
    -   **Where:** Your local terminal.
    -   **What:** Push your branch and its commits to GitHub.
    -   **Command:** `git push -u origin feature/your-branch-name`

### Phase 3: Review & CI (in GitHub)

This phase is about ensuring code quality before it gets merged.

1.  **Open a Pull Request (PR):**
    -   **Where:** GitHub.
    -   **What:** Create a new Pull Request to merge your feature branch into the **`stage` branch**. The PR title should be clear, and the description should again reference the PBI (`AB#123`).

2.  **Automated Checks (Current vs Planned):**
    -   **Current:** GitHub Copilot PR review is configured on GitHub.com and automatically triggers when a PR is opened.
    -   **Planned:** GitHub Actions will provide additional CI checks:
        -   **Linting:** Checks for code style and potential errors.
        -   **Testing:** Runs automated unit and integration tests.
    -   **Result:** The status of these checks will be displayed directly on the PR page. The PR **cannot be merged into `stage`** until these checks pass.

3.  **Code Review:**
    -   **Where:** GitHub.
    -   **What:** (Optional for solo dev, but good practice) Review your own code in the PR to catch any last-minute issues.

### Phase 4: Merge, Deploy, and Promote (GitHub & Azure)

This phase covers merging features, deploying to a staging environment, and promoting to production.

1.  **Merge the Feature PR:**
    -   **Where:** GitHub.
    -   **What:** Once the CI checks are passing, merge the PR into the **`stage` branch**. Use a "Squash and Merge" to keep the `stage` branch history clean with one commit per feature.

2.  **Deployment (Current vs Planned):**
    -   **Current:** No automatic deployment. Manual local testing only.
    -   **Planned:** Automatic Deployment to Staging:
        -   **Where:** Azure App Service (Staging Slot)
        -   **What:** An Azure App Service deployment slot will be configured to monitor the `stage` branch. When it detects the new merge commit, it will automatically deploy the code to a staging environment for final review.

3.  **Promote to Production (Planned):**
    -   **Where:** GitHub
    -   **What:** When you are ready to release, open a new Pull Request to merge the **`stage` branch into the `main` branch**. This PR provides a clear overview of all the features going into the release.
    -   **Process:** After a final check, this PR is merged.

4.  **Automatic Deployment to Production (Planned):**
    -   **Where:** Azure App Service (Production Slot)
    -   **What:** The production App Service will be configured to monitor the `main` branch. When it detects the merge from `stage`, it will automatically pull the latest code and deploy it.

5.  **Close Work Items:**
    -   **Where:** Azure DevOps.
    -   **What:** The PBI and its related Tasks can be automatically moved to the "Done" state by the merge commit to `stage` (if configured) or you can move them manually. This completes the lifecycle.

## Local Development Setup

### Prerequisites
- Python 3.x
- Azure CLI (`az login`)
- Azure Key Vault access

### Environment Configuration
1. Copy `env.example` to `.env`
2. Set `KEY_VAULT_URL` in your `.env` file
3. Ensure you're authenticated with Azure: `az login`
4. The app will automatically fetch Cosmos DB credentials from Key Vault

### Running the Application
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m backend.run

# Or use the development script
./run-dev.sh
```
