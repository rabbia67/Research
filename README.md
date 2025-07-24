# Research Tools

This repository contains Python scripts for research paper analysis and GitHub repository management.

## Components

### 1. Extract Sections from Research Papers (`extract_section_from_research_papers.py`)

A Python script that automatically extracts introduction sections from research papers in PDF and DOCX formats.

#### Features:
- Supports both PDF and DOCX file formats
- Automatically identifies and extracts introduction sections
- Creates a consolidated DOCX file with all extracted introductions
- Smart section detection with configurable patterns
- Progress tracking with tqdm

#### Dependencies:
```bash
pip install pymupdf python-docx tqdm
```

#### Usage:
1. Edit the following variables in the script:
   - `PAPERS_DIR`: Directory containing your research papers
   - `OUT_DOCX`: Output DOCX file path where introductions will be saved

2. Run the script to extract introductions from all papers in the specified directory.

### 2. Git Push Agent (`git_agent.py`)

A Python utility for managing GitHub repositories and automating git operations.

#### Features:
- Create new GitHub repositories
- Automatically push local code to GitHub
- Handle repository authentication
- Error handling and status reporting
- Support for both new and existing repositories

#### Dependencies:
```bash
pip install requests
```

#### Usage:
```python
from git_agent import GitPushAgent

# Initialize the agent
agent = GitPushAgent()

# Push local code to GitHub
agent.push_to_github(
    folder_path="path/to/your/project",
    commit_message="Your commit message",
    auto_create=True  # Will create repo if it doesn't exist
)
```

## Getting Started

1. Clone this repository:
```bash
git clone https://github.com/rabbia67/Research.git
```

2. Install dependencies:
```bash
pip install pymupdf python-docx tqdm requests
```

3. Configure the scripts according to your needs by modifying the relevant variables.

## Note

- For the Git Push Agent, you'll need a GitHub Personal Access Token with 'repo' permissions.
- Make sure you have appropriate permissions for the directories specified in the research paper extraction script.

## Contributing

Feel free to submit issues and pull requests to improve these tools.

## License

This project is available for open use. Please provide attribution when using or modifying the code.