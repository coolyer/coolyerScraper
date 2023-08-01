import requests

def get_latest_version(repo_url):
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            tag_name = data.get('tag_name')
            if tag_name and tag_name.startswith('1.0.0'):
                return tag_name
            else:
                raise ValueError("Invalid or missing version in the GitHub API response.")
        elif isinstance(data, list):
            # Check the releases in reverse order to find the first valid version
            for release in reversed(data):
                tag_name = release.get('tag_name')
                if tag_name and tag_name.startswith('release'):
                    return tag_name
            raise ValueError("Invalid or missing version in the GitHub API response.")
        else:
            raise ValueError("Invalid JSON response from GitHub.")

    except requests.exceptions.RequestException as e:
        print("Error fetching data from GitHub:", e)
        return None
    except (KeyError, ValueError) as e:
        print("Invalid JSON response from GitHub:", e)
        return None


def compare_versions(current_version, latest_version):
    # Assuming versions are in "X.Y.Z" format (e.g., "1.2.3")
    current_parts = list(map(int, current_version.split('.')))
    latest_parts = list(map(int, latest_version.split('.')))

    for i in range(min(len(current_parts), len(latest_parts))):
        if current_parts[i] < latest_parts[i]:
            return -1  # Current version is outdated
        elif current_parts[i] > latest_parts[i]:
            return 1   # Current version is newer

    if len(current_parts) < len(latest_parts):
        return -1  # Current version is outdated
    elif len(current_parts) > len(latest_parts):
        return 1   # Current version is newer

    return 0       # Versions are the same

def version_check(current_version, repo_url):
    latest_version = get_latest_version(repo_url)
    if latest_version:
        comparison = compare_versions(current_version, latest_version)
        if comparison == -1:
            return "Your software is outdated. Please update to the latest version:", latest_version
        elif comparison == 1:
            return "Your software is newer than the latest version:", latest_version
        else:
            return "Your software is up-to-date. Latest version:", latest_version
