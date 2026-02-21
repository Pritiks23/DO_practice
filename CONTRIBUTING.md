# Contributing to DO_practice

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing.

## Development Workflow

### 1. Set Up Your Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/DO_practice.git
cd DO_practice

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write clean, readable code
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run tests
npm test

# Check test coverage
npm run test:coverage

# Lint code
npm run lint

# Type check
npm run typecheck

# Format code
npm run format
```

### 5. Commit Your Changes

We follow conventional commits:

```bash
git commit -m "feat: add new data validation"
git commit -m "fix: resolve memory leak in service"
git commit -m "docs: update API documentation"
git commit -m "test: add integration tests for endpoints"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Build/tool changes

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style Guidelines

### TypeScript

- Use TypeScript strict mode
- Define proper types, avoid `any`
- Use interfaces for object shapes
- Prefer `const` over `let`
- Use arrow functions where appropriate

### Testing

- Write tests for all new features
- Maintain >70% test coverage
- Use descriptive test names
- Test edge cases and error conditions
- Use Jest for unit and integration tests

### File Organization

```
src/
├── __tests__/      # Tests alongside their modules
├── config/         # Configuration files
├── controllers/    # Request handlers
├── middleware/     # Express middleware
├── routes/         # Route definitions
├── services/       # Business logic
├── types/          # TypeScript types
├── utils/          # Utility functions
├── app.ts          # App setup
└── index.ts        # Entry point
```

### Naming Conventions

- Files: camelCase or PascalCase for classes
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE
- Types/Interfaces: PascalCase
- Functions: camelCase, descriptive names

## Pull Request Process

1. **Update documentation** if you've changed APIs or functionality
2. **Add tests** for new features
3. **Ensure all tests pass** locally
4. **Run linter and formatter** before committing
5. **Describe your changes** clearly in the PR description
6. **Reference issues** if applicable (e.g., "Fixes #123")
7. **Wait for review** from maintainers

## Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Linter passes (`npm run lint`)
- [ ] Type checker passes (`npm run typecheck`)
- [ ] Build succeeds (`npm run build`)
- [ ] No security vulnerabilities introduced
- [ ] PR description clearly explains changes

## Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the bug
2. **Steps to reproduce** - Exact steps to reproduce the issue
3. **Expected behavior** - What you expected to happen
4. **Actual behavior** - What actually happened
5. **Environment** - Node version, OS, etc.
6. **Logs/Screenshots** - Any relevant logs or screenshots

## Feature Requests

When requesting features:

1. **Use case** - Explain why this feature would be useful
2. **Proposed solution** - How you think it should work
3. **Alternatives** - Other solutions you've considered
4. **Examples** - Examples from other projects if applicable

## Code Review Process

All submissions require review:

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Changes requested** may need addressing
4. **Approval** required before merging

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the ISC License.
