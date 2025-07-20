import os
import subprocess
import sys
import requests
import json
from getpass import getpass


class GitPushAgent:
    def __init__(self):
        self.github_token = None
        self.username = None

    def get_github_credentials(self):
        """Get GitHub credentials from user"""
        if not self.github_token:
            print("🔐 GitHub authentication required for repository creation")
            print("You need a Personal Access Token with 'repo' permissions")
            print("Create one at: https://github.com/settings/tokens")
            self.github_token = getpass("Enter your GitHub Personal Access Token: ")
            self.username = input("Enter your GitHub username: ")

    def run_git_command(self, cmd, cwd):
        """Execute git command with error handling"""
        try:
            result = subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout.strip():
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            return None

    def create_github_repo(self, repo_name, description="", private=False):
        """Create a new GitHub repository"""
        if not self.github_token or not self.username:
            self.get_github_credentials()

        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": False
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                repo_data = response.json()
                print(f"✅ Repository '{repo_name}' created successfully!")
                return repo_data["clone_url"]
            elif response.status_code == 422:
                error_data = response.json()
                if "already exists" in error_data.get("message", ""):
                    print(f"ℹ️  Repository '{repo_name}' already exists")
                    return f"https://github.com/{self.username}/{repo_name}.git"
                else:
                    print(f"❌ Error creating repository: {error_data.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ Failed to create repository. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None

    def check_repo_exists(self, repo_url):
        """Check if a GitHub repository exists"""
        try:
            # Extract username and repo name from URL
            if "github.com" in repo_url:
                parts = repo_url.replace("https://github.com/", "").replace(".git", "").split("/")
                if len(parts) >= 2:
                    username, repo_name = parts[0], parts[1]

                    # Check if repo exists
                    check_url = f"https://api.github.com/repos/{username}/{repo_name}"
                    response = requests.get(check_url)
                    return response.status_code == 200
        except Exception as e:
            print(f"Warning: Could not check repository existence: {e}")
        return False

    def get_repo_name_from_path(self, folder_path):
        """Extract repository name from folder path"""
        return os.path.basename(os.path.abspath(folder_path))

    def push_to_github(self, folder_path, commit_message="Auto commit from agent", auto_create=True):
        """Main function to push code to GitHub with optional repo creation"""
        if not os.path.isdir(folder_path):
            print("❌ Invalid folder path.")
            return False

        print(f"🚀 Starting Git push process for: {folder_path}")

        # Initialize Git repo if not already
        if not os.path.isdir(os.path.join(folder_path, '.git')):
            print("📁 Initializing new Git repository...")
            if not self.run_git_command(["git", "init"], folder_path):
                return False
            if not self.run_git_command(["git", "checkout", "-b", "main"], folder_path):
                return False

        # Add all files
        print("📝 Adding changes...")
        if not self.run_git_command(["git", "add", "."], folder_path):
            return False

        # Commit only if changes are staged
        print("📦 Checking for changes to commit...")
        diff_result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=folder_path)
        if diff_result.returncode != 0:
            if not self.run_git_command(["git", "commit", "-m", commit_message], folder_path):
                return False
        else:
            print("ℹ️  No changes to commit.")

        # Handle remote repository
        remotes = subprocess.run(["git", "remote"], cwd=folder_path, capture_output=True, text=True)

        if "origin" not in remotes.stdout:
            # No remote set, need to configure one
            repo_name = self.get_repo_name_from_path(folder_path)

            if auto_create:
                print(f"🔍 No remote repository found. Attempting to create '{repo_name}' on GitHub...")

                # Get repository details
                description = input(f"📝 Enter description for '{repo_name}' (optional): ").strip()
                private_input = input("🔒 Make repository private? (y/N): ").strip().lower()
                private = private_input in ['y', 'yes']

                # Create repository
                remote_url = self.create_github_repo(repo_name, description, private)

                if not remote_url:
                    print("❌ Failed to create repository. Please create it manually.")
                    remote_url = input("🔗 Enter GitHub repository URL manually: ")
            else:
                remote_url = input("🔗 Enter GitHub repository URL: ")

            if remote_url:
                if not self.run_git_command(["git", "remote", "add", "origin", remote_url], folder_path):
                    return False
            else:
                print("❌ No repository URL provided. Cannot proceed.")
                return False

        # Push to GitHub
        print("🚀 Pushing to GitHub...")
        push_result = self.run_git_command(["git", "push", "-u", "origin", "main"], folder_path)

        if push_result:
            print("✅ Successfully pushed to GitHub!")
            # Get the repository URL for display
            remote_url = subprocess.run(["git", "remote", "get-url", "origin"],
                                        cwd=folder_path, capture_output=True, text=True)
            if remote_url.stdout.strip():
                repo_url = remote_url.stdout.strip().replace('.git', '')
                print(f"🌐 Repository URL: {repo_url}")
            return True
        else:
            print("❌ Failed to push to GitHub.")
            return False


def main():
    agent = GitPushAgent()

    # Configuration
    print("🔧 Git Push Agent - Enhanced Version")
    print("=" * 40)

    # Get folder path
    default_path = r"C:\Users\Rabbia\Desktop\git data\Computer-Science"
    folder_path = input(f"📁 Enter folder path (default: {default_path}): ").strip()

    if not folder_path:
        folder_path = default_path

    # Get commit message
    commit_message = input("💬 Enter commit message (default: 'Auto commit from agent'): ").strip()
    if not commit_message:
        commit_message = "Auto commit from agent"

    # Auto-create repository option
    auto_create_input = input("🤖 Auto-create repository if it doesn't exist? (Y/n): ").strip().lower()
    auto_create = auto_create_input not in ['n', 'no']

    # Execute push
    success = agent.push_to_github(folder_path, commit_message, auto_create)

    if success:
        print("\n🎉 Process completed successfully!")
    else:
        print("\n❌ Process failed. Please check the errors above.")


if __name__ == "__main__":
    main()