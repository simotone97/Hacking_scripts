import requests
import os

# Set your GitHub token here
GITHUB_TOKEN = 'TOKEN_HERE'
BASE_API_URL = 'https://api.github.com'

def get_repositories(username):
    """Return the repos list of a user."""
    url = f'{BASE_API_URL}/users/{username}/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting the repositories: {response.status_code}")
        return []

def get_files_in_repository(username, repo_name):
    """Return the list of files in a repository."""
    url = f'{BASE_API_URL}/repos/{username}/{repo_name}/git/trees/main?recursive=1'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('tree', [])
    else:
        print(f"Error getting the files for the repository: {repo_name}: {response.status_code}")
        return []

def get_raw_links(username):
    repos = get_repositories(username)
    raw_links = []

    for repo in repos:
        repo_name = repo['name']
        files = get_files_in_repository(username, repo_name)

        for file in files:
            if file['type'] == 'blob':  # Solo file, non cartelle
                raw_url = f'https://raw.githubusercontent.com/{username}/{repo_name}/main/{file["path"]}'
                raw_links.append(raw_url)

    return raw_links

def download_file(url, save_path):
    """Download a file from a URL and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded: {save_path}")
    else:
        print(f"Failed to download {url}: {response.status_code}")

# Example of usage
if __name__ == "__main__":
    github_username = 'USERNAME_HERE'  # Insert here the GitHub username you want to scrape
    raw_links = get_raw_links(github_username)

    for link in raw_links:
        print(link)

    user_approval = input("Do you want to download these files? (yes/no): ").strip().lower()

    if user_approval == 'yes':
        save_directory = "downloaded_files"
        os.makedirs(save_directory, exist_ok=True)

        for link in raw_links:
            filename = os.path.join(save_directory, link.split('/')[-1])
            download_file(link, filename)
    else:
        print("Download aborted.")

    raw_links = get_raw_links(github_username)
    
    for link in raw_links:
        print(link)
