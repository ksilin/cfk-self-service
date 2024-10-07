from github import Github
import base64
import os


def prepare_pr_details(prefix, topic_name):
    """
    Prepare details for creating a pull request.

    Args:
        prefix (str): Prefix for the topic name.
        topic_name (str): Original topic name.

    Returns:
        dict: Dictionary containing branch name, PR title, PR body, and filename.
    """
    branch_name = f"add-topic-{prefix}{topic_name}"
    pr_title = f"Add Kafka topic YAML for {prefix}{topic_name}"
    pr_body = "This pull request adds a new Kafka topic definition."
    filename = f"topics/{prefix}{topic_name}.yaml"

    return {
        "branch_name": branch_name,
        "pr_title": pr_title,
        "pr_body": pr_body,
        "filename": filename
    }

def create_branch_and_pr(github_token, repository_name, branch_name, filename, content, pr_title, pr_body):
    """
    Create a new branch and a pull request with the specified content in the GitHub repository.

    Args:
        github_token (str): Personal access token for GitHub API authentication.
        repository_name (str): The full name of the GitHub repository (e.g., "user/repo").
        branch_name (str): The name of the new branch to create.
        filename (str): The file path to be created in the branch.
        content (str): The content of the file to be committed.
        pr_title (str): Title of the pull request.
        pr_body (str): Body description of the pull request.

    Returns:
        str: URL of the created pull request.
    """
    g = Github(github_token)
    repo = g.get_repo(repository_name)

    source = repo.get_branch("main")

    try:
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
    except Exception as e:
        raise Exception(f"Error creating branch: {str(e)}")

    try:
        repo.create_file(
            path=filename,
            message=f"Add Kafka topic YAML: {filename}",
            content=content,
            branch=branch_name
        )
    except Exception as e:
        raise Exception(f"Error creating or updating file: {str(e)}")

    try:
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base="main"
        )
        return pr.html_url
    except Exception as e:
        raise Exception(f"Error creating pull request: {str(e)}")
