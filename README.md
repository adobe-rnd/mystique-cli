# Coda: AI-Powered Coding Assistant

## Overview

This command line tool is a general-purpose AI-powered coding assistant that makes it super easy to generate, modify, and enhance code. By using Generative AI, it helps developers quickly create, tweak, and improve various code components. It's a simple project designed to show how easy it is to build such a tool from scratch and also to serve as a foundation for custom implementations.

## Installation

To install the command line tool from PyPI, run:

```bash
pip install coda-ai-assistant
```

## Configuration

When you first run the tool, it will automatically create a `config.json` file in the `.coda` directory in your project's root. You don't need to create this file manually - the application will guide you through the setup process by prompting you to:

1. Choose your preferred API provider (OpenAI or Azure)
2. Enter the necessary API keys and configuration values
3. Save the configuration automatically

## Usage

To use the command line tool, execute the following command from the root directory of the project you want to modify:

```bash
coda
```

Follow the on-screen prompts to interact with the tool, generate code, and apply changes to your project.

## Features

- **AI-Powered Assistance**: Demonstrates how to implement AI-powered coding support for various projects.
- **Foundation for Custom Tools**: Provides a starting point for building personalized coding assistants.
- **Automatic File Detection**: Identifies the necessary files for modification automatically.
- **Rollback Support**: Includes functionality to revert changes if needed.
- **API Compatibility**: Works seamlessly with both Azure OpenAI and OpenAI API configurations.

## Building and Publishing to PyPI

To build and publish the package to PyPI using Poetry and an API token, follow these steps:

1. Ensure you have Poetry installed. If not, install it by following the instructions at [Poetry's official website](https://python-poetry.org/docs/#installation).

2. Configure Poetry to use your PyPI token:
    ```bash
    poetry config pypi-token.pypi <your-pypi-token>
    ```

3. Build and publish the package to PyPI:
    ```bash
    poetry publish --build
    ```

Replace the placeholder values with your actual API keys and endpoints.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
