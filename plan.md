# Implementation Plan

**At Startup:**

- Perform an initial indexing of the project's source files:
    - For each file (`*.js`, `*.html`, `*.css`):
        - Generate a concise summary of the file content.
        - Create a vector representation of this summary.
        - Store the vector representation in a database.

- Start the preview server:
    - Execute the `aem up` command to preview changes in the browser.

**Main Loop:**

- For each user prompt:
    - Generate a vector representation of the prompt.
    - Retrieve the N most similar files from the database.
    - Formulate a prompt for the LLM using the user prompt and the retrieved files to produce a diff for the solution.
    - Store the diff in the database for each iteration.
    - Apply the diff to all relevant files to create a new version.

**Rollback Process:**

- If the user is not satisfied with the changes:
    - Retrieve the diff from the database.
    - Apply the diff to the files to revert the changes.

Here is the updated UX requirements in the concise format you provided:

### **UX:**
- Create a CLI interface for user interaction.
- The app should run in a continuous loop until the user chooses to exit.
- The app should be able to:
  - **Run/Re-run Indexing:**
    - If indexing data is missing, prompt the user to run indexing.
  - **Prompt for Changes:**
    - Ask the user for a description or prompt to make a change.
  - **Display Changed Files:**
    - Show a list of files that were changed after the prompt.
  - **Apply or Reject Changes:**
    - Ask the user whether they want to accept or reject the changes.
  - **Rollback Changes:**
    - Provide an option to rollback the most recent change; only enabled if there are changes to roll back.
  - **Reindex:**
    - Offer an option to reindex at any point during the main loop.
  - **Exit the App:**
    - Ask the user if they want to exit the application, confirming before exiting.

Requrements:
- Use Azure OpenAI API for the LLM (generation and embedings).
- Use langchain for the vectorization of the files including chunking.
- Configure tools for LLM and langchain.
