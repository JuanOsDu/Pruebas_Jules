# Pull Request Guidelines

When creating a pull request, please adhere to the following guidelines:

*   **Commit Message Format:** The commit message should follow the Conventional Commits specification.
    *   The subject line must be at most 79 characters long.
    *   The format should be `type(scope): RTS-XXXX description`.
    *   `type` can be one of: `feat`, `chore`, `fix`, `docs`, `refactor`.
    *   `scope` refers to the module or part of the codebase affected by the change.
    *   `RTS-XXXX` is the ticket number associated with the change.
    *   `description` is a short summary of the changes.

    **Example:**
    ```
    feat(parser): RTS-1234 Add support for new data format
    ```
*   **Pull Request Title:** The pull request title should match the commit message subject line.
*   **Pull Request Description:** The pull request description should provide a detailed explanation of the changes, including the problem being solved, the solution implemented, and any relevant context.
*   **Testing:** All changes should be accompanied by relevant tests. Ensure that all existing tests pass before submitting the pull request.
*   **Branch Naming:** The branch name should be the ticket number in the format `RTS-XXXX`.
