# Contributing to RavenChain

First off, thank you for considering contributing to RavenChain! It's people like you that make RavenChain such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include details about your configuration and environment

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed functionality
* Explain why this enhancement would be useful
* List any additional requirements

### Pull Requests

* Fill in the required template
* Follow the Python style guides
* Include appropriate test cases
* Update documentation as needed

## Development Process

1. Fork the repo
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Format your code (`black .`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ravenchain.git
cd ravenchain

# Ensure you have Python 3.13+ installed
python --version

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific.py

# Run with coverage
pytest --cov=ravenchain
```

## Style Guide

This project uses:
* Black for code formatting
* isort for import sorting
* pylint for code quality

## Documentation

* Use docstrings for all public modules, functions, classes, and methods
* Follow Google style for docstrings
* Keep the README.md up to date

## Blockchain-Specific Guidelines

When contributing to RavenChain, please consider:

### Security
* All cryptographic operations must be thoroughly reviewed
* Avoid introducing new dependencies without careful consideration
* Always validate input data

### Performance
* Consider the impact of changes on block validation speed
* Test with realistic blockchain sizes
* Profile code changes that might impact performance

### Consensus
* Changes to consensus rules require extensive discussion
* Backward compatibility must be considered
* Document any changes to the protocol

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.
