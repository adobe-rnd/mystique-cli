# Coda: AI-Powered Coding Assistant

## Overview

> This command line tool is a general-purpose AI-powered coding assistant that makes it super easy to generate, modify, and enhance code. By using Generative AI, it helps developers quickly create, tweak, and improve various code components. It's a simple project designed to show how easy it is to build such a tool from scratch and also to serve as a foundation for custom implementations.

## Features

- **AI-Powered Help**: Easily add AI-driven coding support to your projects.
- **Custom Tool Foundation**: A great starting point for creating your own coding assistants.
- **Smart File Detection**: Automatically finds the files you need to work on.
- **Undo Changes**: Built-in support to revert changes if something goes wrong.
- **API Flexibility**: Works smoothly with both Azure OpenAI and OpenAI APIs.

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

```
_________     _________       
__  ____/___________  /_____ _
_  /    _  __ \  __  /_  __ `/
/ /___  / /_/ / /_/ / / /_/ / 
\____/  \____/\__,_/  \__,_/  
          
Configuration folder: /Users/vitaly/Projects/coda/.coda
Project directory: /Users/vitaly/Projects/coda
API Provider: OpenAI

? Choose an action: 
❯ Modify files using a prompt
  Reindex project files
  Change settings
  Exit
```

## Additional Context

To provide additional context about the structure of the project, you can add text files to the `context` folder inside the `.coda` directory. These files will be read and used by the application to enhance its understanding of your project.

### Steps to Add Additional Context

1. Navigate to the `.coda` directory in your project root.
2. Create a folder named `context` if it doesn't already exist.
3. Add any `.txt` files containing the additional context you want to include.

Example:
```
.coda/
├── config.json
└── context/
    ├── project_structure.txt
    └── coding_guidelines.txt
```

### Use Cases for Adding Additional Context

- **Project Structure**: Describe the overall structure of the project, including key directories and files.
- **Coding Guidelines**: Provide coding standards and best practices to be followed.
- **API Documentation**: Include details about the APIs used in the project.
- **Setup Instructions**: Add instructions for setting up the development environment.

The content of these files will be included in the prompt used by the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
