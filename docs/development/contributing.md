# Contributing to DSGVO-Checker

## Overview

Thank you for your interest in contributing to DSGVO-Checker! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key (for testing)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DSGVO-Checker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Code Style Guidelines

### Python Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused on a single responsibility

### Documentation

- Write documentation in English
- Use clear, concise language
- Include code examples where appropriate
- Update documentation when adding new features

### Error Handling

- Use proper exception handling
- Log errors with appropriate log levels
- Provide user-friendly error messages
- Avoid using `print()` for errors in production code

## Testing

### Running Tests

```bash
# Test installation
python test_installation.py

# Test proxy connection
python test_proxy.py
```

### Writing Tests

- Write tests for new functionality
- Test both success and error cases
- Use descriptive test names
- Mock external dependencies when appropriate

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   python test_installation.py
   streamlit run app.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commit format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

## Architecture Guidelines

### Modular Design

- Keep components loosely coupled
- Use dependency injection where appropriate
- Follow the single responsibility principle
- Maintain clear interfaces between modules

### Configuration Management

- Use environment variables for configuration
- Provide sensible defaults
- Validate configuration on startup
- Document all configuration options

### Error Handling

- Use structured logging
- Provide meaningful error messages
- Handle edge cases gracefully
- Implement proper cleanup in error scenarios

## Security Considerations

### Data Privacy

- Never log sensitive data
- Validate all user inputs
- Use secure file handling
- Implement proper access controls

### API Security

- Validate API keys
- Implement rate limiting
- Use HTTPS for all external communications
- Sanitize all inputs

## Performance Guidelines

### Optimization

- Profile code for bottlenecks
- Use efficient data structures
- Implement caching where appropriate
- Optimize database queries (if applicable)

### Resource Management

- Close file handles properly
- Use context managers for resource management
- Implement proper cleanup in destructors
- Monitor memory usage

## Documentation

### Code Documentation

- Write clear docstrings
- Include type hints
- Document complex algorithms
- Provide usage examples

### User Documentation

- Keep documentation up to date
- Include screenshots for UI changes
- Provide step-by-step instructions
- Include troubleshooting guides

## Release Process

### Version Management

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version numbers in all relevant files
- Create release notes for each version
- Tag releases in Git

### Deployment

- Test in staging environment
- Use Docker for consistent deployments
- Implement health checks
- Monitor application performance

## Getting Help

- Check existing issues before creating new ones
- Use the issue template when reporting bugs
- Provide detailed information when reporting issues
- Be respectful and constructive in discussions

## Code of Conduct

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and open to feedback
- Focus on what is best for the community

Thank you for contributing to DSGVO-Checker! 