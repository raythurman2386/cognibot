# Style Guidelines for Cognibot

To maintain consistency and readability across the Cognibot project, we adhere to the following style guidelines. We use Black, an opinionated code formatter, to automatically format our Python code.

## Python Code Formatting

### Black

We use Black to automatically format our Python code. Black is an uncompromising code formatter that adheres to PEP 8 guidelines with some modifications.

- **GitHub Action**: We have a GitHub Action set up to run Black on all pull requests. This ensures that all code merged into the main branch is consistently formatted.

- **Local Usage**: To format your code locally before committing, ensure your virutal environment is activated and run the following command:

```
black .
```

### Additional Style Guidelines

While Black takes care of most formatting concerns, here are some additional guidelines to follow:

1. **Imports**:

   - Use absolute imports.
   - Group imports in the following order: standard library, third-party libraries, local application imports.
   - Within each group, sort imports alphabetically.

2. **Docstrings**:

   - Use Google-style docstrings for functions, classes, and modules.
   - Include type hints in function signatures rather than in docstrings.

3. **Comments**:

   - Try not to use comments unless necessary.
   - Write clear, concise comments for complex logic.
   - Keep comments up-to-date with code changes.

4. **Naming Conventions**:

   - Classes: CapWords convention (e.g., `MyClass`)
   - Functions and variables: lowercase with underscores (e.g., `my_function`, `my_variable`)
   - Constants: ALL_CAPS with underscores (e.g., `MAX_VALUE`)

5. **Type Hints**:
   - Use type hints for function arguments and return values.
   - Use `Optional[Type]` for arguments that can be None.

## Git Commit Messages

- Write clear, concise commit messages in the imperative mood.
- Gitmoji is a popular emoji for commit messages and I personally use it but not required
