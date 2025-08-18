# 🏪 Scraper Simple de Títulos - MercadoLibre

Extrae únicamente los títulos de productos de MercadoLibre de forma rápida y sencilla.

## ⚡ Uso rápido (CLI)

```bash
# Instalar dependencias
pip install requests beautifulsoup4

# Ejecutar scraper
python scrapper.py "notebook" 3

# Ejemplos
python scrapper.py "celular samsung"
python scrapper.py "zapatos nike" 5
python scrapper.py "carro usado" 2
```

## 🚀 API Usage

The project also provides a web scraping API that allows you to extract information from websites.

### Scrape a URL

*   **Endpoint:** `/scrape`
*   **Method:** `GET`
*   **Description:** Scrapes a given query and returns the results.
*   **Parameters:**
    *   `query` (string, required): The search term to scrape.
    *   `pages` (integer, optional, default: 1): The number of pages to scrape.
*   **Example Request:**
    ```bash
    curl "http://localhost:8000/scrape?query=fastapi&pages=2"
    ```
*   **Success Response:**
    ```json
    {
        "status": "success",
        "output": "...",
        "file_saved": "titulos_fastapi.txt"
    }
    ```
*   **Error Response:**
    ```json
    {
        "status": "error",
        "message": "...",
        "output": "...",
        "exit_code": 1
    }
    ```

## 🤖 Configuring AGENTS.md

The `AGENTS.md` file is used to provide instructions to the AI agent (Jules) on how to interact with the repository.

### How it Works

The agent automatically detects and reads any `AGENTS.md` file within the repository's file hierarchy. The instructions in an `AGENTS.md` file apply to the entire directory tree where it's located. If there are multiple `AGENTS.md` files in different directories, the instructions in the most deeply nested file take precedence.

### Example `AGENTS.md`

You can create an `AGENTS.md` file in the root of the project with the following content to define pull request guidelines:

```markdown
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
```
By using the `AGENTS.md` file, you can ensure that the agent follows your project's conventions.
