# Testing Guidelines for Cognibot

We use pytest for running our test suite and measuring code coverage. Our goal is to maintain high test coverage and ensure the reliability of our codebase.

## Running Tests

To run the test suite, use the following command:

```
pytest --cov=. tests/
```

This command runs all tests in the `tests/` directory and generates a coverage report.

## Test Configuration

We use a `pytest.ini` file to configure our test environment.

This configuration sets up the Python path, configures asyncio testing, ignores UserWarnings, excludes certain directories and files, and sets up coverage reporting.

## Test Coverage

We aim for a minimum of 80% test coverage across the entire project. As of the last update, our overall coverage is 88%, which is good, but there's room for improvement in some modules.

### Current Coverage Overview

- Overall coverage: 88%
- Modules with 100% coverage:
  - `cogs/fun.py`
  - `cogs/greetings.py`
  - `db/backup.py`
- Modules needing improvement:
  - `cogs/openai.py` (48% coverage)
  - `utils/logger.py` (76% coverage)
  - `cogs/anthropic.py` (83% coverage)

## Writing Tests

1. **Test File Structure**:

   - Place test files in the `tests/` directory.
   - Name test files with the prefix `test_` (e.g., `test_database.py`).

2. **Test Naming Convention**:

   - Use descriptive names for test functions, prefixed with `test_`.
   - Example: `test_user_registration_success`

3. **Test Coverage**:

   - Aim to cover all branches and edge cases.
   - Include both positive and negative test cases.

4. **Mocking**:

   - Use `unittest.mock` or `pytest-mock` for mocking external dependencies.
   - Ensure mocks accurately represent the behavior of the real objects.

5. **Fixtures**:

   - Use pytest fixtures for setting up test data or objects.
   - Currently, fixtures are defined in individual test files.
   - **Optimization Opportunity**: Consider creating a `conftest.py` file in the `tests/` directory to store common fixtures. This will improve reusability and reduce code duplication across test files.

6. **Async Testing**:
   - Use `pytest.mark.asyncio` decorator for testing asynchronous functions.
   - Utilize `asyncio` and `anyio` plugins for async support (already configured in `pytest.ini`).

## Improving Test Coverage

To improve our test coverage:

1. Focus on `cogs/openai.py`:

   - Add tests for missing lines 34, 61-71, 74-75, 82-99, 107-127, 130-138, 141-153.
   - Prioritize testing the core functionality and edge cases.

2. Enhance `utils/logger.py`:

   - Add tests for lines 21-22, 25-26, 43, 64-67, 70-71.
   - Ensure logging behavior is correctly tested.

3. Complete coverage for `cogs/anthropic.py`:
   - Add tests for lines 43-44, 57-70.

## Continuous Integration

We use GitHub Actions to run our test suite on every pull request. Ensure all tests pass before merging any changes.

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on the state from other tests.
2. **Readability**: Write clear, concise tests that are easy to understand.
3. **Maintenance**: Keep tests up-to-date with code changes.
4. **Performance**: Optimize tests to run quickly, especially for CI/CD pipelines.
5. **Common Fixtures**: Move common fixtures to a `conftest.py` file to improve code reuse and maintainability.

## Reporting Issues

If you encounter any issues with the tests or have suggestions for improving our testing process, please open an issue on GitHub.

Remember, thorough testing is crucial for maintaining the reliability and stability of Cognibot. Always consider adding or updating tests when implementing new features or fixing bugs.

## Future Optimizations

1. **Create `conftest.py`**: Implement a `conftest.py` file in the `tests/` directory to store common fixtures and reduce code duplication across test files.
2. **Review Excluded Directories**: Periodically review the `norecursedirs` and `exclude` settings in `pytest.ini` to ensure they're up-to-date with the project structure.
3. **Optimize Test Performance**: Regularly profile test execution times and optimize slow tests to maintain a fast CI/CD pipeline.
