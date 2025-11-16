import requests
import json
import os

GITHUB_API = "https://api.github.com/users/{}"

def fetch_profile(username):
    """Fetch basic user profile"""
    url = GITHUB_API.format(username)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile: {response.status_code}")

    return response.json()


def fetch_repos(username):
    """Fetch all repositories of the user"""
    url = GITHUB_API.format(username) + "/repos"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch repos: {response.status_code}")

    return response.json()


def save_raw(username, profile, repos):
    """Save raw JSON to disk for Member 2"""
    folder = "analysis"
    path = os.path.join(folder, "raw_data.json")

    data = {
        "profile": profile,
        "repos": repos
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Raw data saved to: {path}")


def fetch_and_save(username):
    """Main function for Member 1 workflow"""
    print("Fetching GitHub data...")

    profile = fetch_profile(username)
    repos = fetch_repos(username)

    save_raw(username, profile, repos)

    print("Done! Member 2 can now process analysis/raw_data.json")


if __name__ == "__main__":
    user = input("Enter GitHub username: ")
    fetch_and_save(user)
