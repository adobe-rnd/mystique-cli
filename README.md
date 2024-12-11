# AI-Powered Coding Assistant

## Overview

This command line tool is a general-purpose AI-powered coding assistant that makes it super easy to generate, modify, and enhance code. By using Generative AI, it helps developers quickly create, tweak, and improve various code components. It's a simple project designed to show how easy it is to build such a tool from scratch and also to serve as a foundation for custom implementations.

## Installation

To install the command line tool locally from the current project folder, run:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the root of your project and add the necessary environment variables to configure the tool. Below is an example of the `.env` file structure:

### Example `.env` File

```plaintext
AZURE_OR_OPENAI=your_provider_choice

# Azure Configuration
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=your_azure_endpoint
AZURE_COMPLETION_DEPLOYMENT=your_azure_completion_deployment
AZURE_EMBEDDING_DEPLOYMENT=your_azure_embedding_deployment

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder values with your actual API keys and endpoints.

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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
