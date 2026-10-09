# idea-sync - Agent Instructions

Here is the `Agents.md` file structured according to the provided requirements:

```markdown
# Agents

## Project Overview and Purpose
Idea-Sync aims to provide a seamless way for users to synchronize their ideas across different platforms, such as Android devices. The project focuses on creating an intuitive user interface that allows users to input and manage their ideas efficiently.

## Tech Stack and Dependencies
- Python 3.x
- Kivy (for the Android app frontend)
- Pytest (for testing)
- Flask (for backend API)

## Key File Patterns (Globs)
- `*.py`: All Python files.
- `tests/`: Directory containing test files for unit testing.

## Build/Test Commands
### Backend:
```bash
python -m unittest discover tests/
```

### Frontend (Android):
```bash
python android_app.py
```

### Full Project:
```bash
pipenv run pytest
```

## Important Notes for AI Agents
- Ensure all input is sanitized to prevent injection attacks.
- Use a consistent logging strategy across the project.
- Implement error handling for user inputs and API responses.

## Coding Conventions
1. **Imports**: Place imports at the top of each Python file in alphabetical order.
2. **Function/Method Naming**:
   - Functions should be named descriptively, starting with a lowercase letter.
   - Method names should follow the same convention as functions but start with an uppercase letter.
3. **Comments**: Use comments to explain complex logic or non-obvious parts of code.
4. **Code Style**:
   - Follow PEP 8 for Python style guide.
   - Ensure consistent indentation (use 4 spaces).
5. **Versioning**: Use semantic versioning (MAJOR.MINOR.PATCH) for all releases.

## Additional Notes
- The project uses Flask as the backend API, which should be tested thoroughly to ensure robustness and security.
- For Android app development, Kivy is used, ensuring a smooth user experience on mobile devices.
```

This `Agents.md` file provides comprehensive documentation covering the specified sections. It serves as an essential reference for developers working on the project, ensuring consistency in coding practices and providing clear instructions for building and testing the system.