# Contributing to Cognibot

We're excited that you're interested in contributing to Cognibot! This guide will help you get started with the contribution process.

## Getting Started

1. **Join our Community**

   - Join our [Discord server](https://discord.gg/MxNVnrxJJw) to connect with other contributors and get support.

2. **Fork the Repository**

   - Visit the [Cognibot GitHub repository](https://github.com/raythurman2386/cognibot).
   - Click the "Fork" button in the top-right corner to create your own copy of the repository.

3. **Clone Your Fork**

   ```
   git clone https://github.com/your-username/cognibot.git
   cd cognibot
   ```

4. **Set Up Development Environment**
   - Follow the [Installation Guide](https://github.com/raythurman2386/cognibot/wiki/Developer-Setup) to set up your local development environment.
   - Check out the Documentation directory and make sure you can run the bot locally before making changes.

## Making Changes

1. **Create a New Branch**

   ```
   git checkout -b your-branch-name
   ```

   Name your branch something descriptive related to your changes.

2. **Make Your Changes**

   - Write your code following the [Style Guidelines](https://github.com/raythurman2386/cognibot/wiki/Style-Guidelines).
   - Ensure your changes are focused and address a specific issue or feature.

3. **Test Your Changes**

   - Run the existing test suite:
     ```
     pytest --cov=. tests/
     ```
   - Add new tests for your changes if applicable.
   - Ensure all tests pass and there's no reduction in code coverage.

4. **Commit Your Changes**

   ```
   git add .
   git commit -m "Your descriptive commit message"
   ```

   - Write clear, concise commit messages.
   - Reference any related issues in your commit message (e.g., "Fixes #123").

5. **Push to Your Fork**
   ```
   git push origin your-branch-name
   ```

## Submitting a Pull Request

1. **Create a Pull Request**

   - Go to the [Cognibot repository](https://github.com/raythurman2386/cognibot) on GitHub.
   - Click "New Pull Request".
   - Select your branch and fill out the PR template.

2. **Describe Your Changes**

   - Provide a clear title and description for your PR.
   - Explain the purpose of your changes and how you tested them.
   - Link any related issues.

3. **Code Review**

   - Be responsive to any feedback or questions from reviewers.
   - Make any requested changes and push them to your branch.

4. **Merge**
   - Once approved, a maintainer will merge your PR.
   - Celebrate your contribution! 🎉

## Additional Guidelines

- **Code Style**: We use Black for code formatting. Run `black .` before committing to ensure consistent style.
- **Documentation**: Update relevant documentation if your changes affect user-facing features or APIs.
- **Commit History**: Keep your commit history clean and meaningful. Squash commits if necessary before submitting your PR.
- **Issue Tracking**: For new features or significant changes, create an issue first to discuss the proposed changes.

## Getting Help

- If you're stuck or have questions, don't hesitate to ask in our [Discord server](https://discord.gg/MxNVnrxJJw).
- Check out the [FAQ](link-to-faq) for common questions and issues.
- For bug reports or feature requests, please [create an issue](https://github.com/raythurman2386/cognibot/issues/new) on GitHub.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. By participating in the Cognibot project, you agree to abide by our Code of Conduct:

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or electronic address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [INSERT EMAIL ADDRESS]. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident.
