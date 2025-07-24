# Git Push Agent

A robust Python utility for automating GitHub repository management and git operations. This tool simplifies the process of creating repositories, initializing git, and pushing code to GitHub.

## Features

- 🔐 Secure GitHub authentication using Personal Access Tokens
- 🚀 Automated repository creation on GitHub
- 📁 Git initialization and configuration
- 🔄 Smart handling of existing repositories
- 💬 Customizable commit messages
- 🔒 Support for both public and private repositories
- ⚡ Command-line interface for easy interaction
- 🛠️ Error handling and detailed status reporting
- 🔍 Repository existence checking
- 📝 Optional repository descriptions

## Installation

1. Ensure you have Python installed on your system
2. Install required dependencies:
```bash
pip install requests
```

## Usage

### As a Command-Line Tool

Run the script directly from the command line:

```bash
python git_agent.py
```

The interactive CLI will guide you through:
1. Entering the folder path (or using default)
2. Providing a commit message
3. Choosing whether to auto-create repository
4. Handling authentication

### As a Python Module

```python
from git_agent import GitPushAgent

# Initialize the agent
agent = GitPushAgent()

# Basic usage
agent.push_to_github(
    folder_path="/path/to/your/project",
    commit_message="Initial commit",
    auto_create=True
)

# Create a private repository with description
repo_url = agent.create_github_repo(
    repo_name="my-project",
    description="A fantastic project",
    private=True
)
```

## Authentication

The agent requires a GitHub Personal Access Token with 'repo' permissions:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate a new token with 'repo' scope
3. When running the script, you'll be prompted to enter:
   - Your GitHub Personal Access Token
   - Your GitHub username

## API Reference

### GitPushAgent Class

#### `__init__()`
Initializes the agent with empty credentials.

#### `push_to_github(folder_path, commit_message="Auto commit from agent", auto_create=True)`
Main method to push code to GitHub.

Parameters:
- `folder_path`: Path to the local repository
- `commit_message`: Custom commit message (default: "Auto commit from agent")
- `auto_create`: Whether to create repository if it doesn't exist (default: True)

Returns: `bool` - Success status

#### `create_github_repo(repo_name, description="", private=False)`
Creates a new GitHub repository.

Parameters:
- `repo_name`: Name for the new repository
- `description`: Repository description (optional)
- `private`: Whether the repository should be private (default: False)

Returns: Repository clone URL or None if failed

#### `check_repo_exists(repo_url)`
Checks if a GitHub repository exists.

Parameters:
- `repo_url`: GitHub repository URL

Returns: `bool` - Whether repository exists

## Example Workflows

### 1. New Project Setup

```python
agent = GitPushAgent()
agent.push_to_github(
    folder_path="/path/to/new/project",
    commit_message="Initial project setup",
    auto_create=True
)
```

### 2. Working with Existing Repository

```python
agent = GitPushAgent()
agent.push_to_github(
    folder_path="/path/to/existing/project",
    commit_message="Updated features",
    auto_create=False
)
```

## Error Handling

The agent includes comprehensive error handling for common scenarios:
- Invalid folder paths
- Network issues
- Authentication failures
- Repository creation conflicts
- Git command failures

Each error provides descriptive messages and appropriate exit paths.

## Best Practices

1. Always store GitHub tokens securely
2. Use descriptive commit messages
3. Verify folder paths before pushing
4. Use try-except blocks when using as a module
5. Check repository existence before operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open-source and available for free use. Please provide attribution when using or modifying the code.
