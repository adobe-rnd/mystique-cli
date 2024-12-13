# Coda: AI-Powered Coding Assistant

## Overview

> This command line tool leverages AI to assist with coding tasks, making it easy to generate, modify, and enhance code. Utilizing Generative AI, it helps developers quickly create, adjust, and improve various code components. This project demonstrates the simplicity of building such a tool from scratch and serves as a foundation for custom implementations.

## Features

- **Smart File Detection**: Automatically identifies the files you need to work on.
- **Undo Changes**: Easily revert changes if something goes wrong.
- **API Flexibility**: Compatible with both Azure OpenAI and OpenAI APIs.
- **Respects .gitignore**: Excludes files and directories specified in `.gitignore` during indexing.
- **Custom Tool Foundation**: A solid starting point for creating your own coding assistants.

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
