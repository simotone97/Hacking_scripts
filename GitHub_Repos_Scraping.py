import requests

# Setup your GitHub token here
GITHUB_TOKEN = 'your_github_token_here'
BASE_API_URL = 'https://api.github.com'

def get_repositories(username):
    """return the repos list of a user."""
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
    """return the list of files in a repository."""
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
            if file['type'] == 'blob':  # solo file, non cartelle
                raw_url = f'https://raw.githubusercontent.com/{username}/{repo_name}/main/{file["path"]}'
                raw_links.append(raw_url)
    
    return raw_links

# Example of usage
if __name__ == "__main__":
    github_username = 'username_here' #insert here the GitHub username you want to scratch
    raw_links = get_raw_links(github_username)
    
    for link in raw_links:
        print(link)
