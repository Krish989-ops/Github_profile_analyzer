# test_api.py
from github_api import fetch_user_data, fetch_repos_data
import json

def main():
    username = input("Enter GitHub username: ")
    user_data = fetch_user_data(username)
    repos_data = fetch_repos_data(username)

    # Save data locally for the analysis team
    with open(f"{username}_data.json", "w") as f:
        json.dump({
            "user": user_data,
            "repos": repos_data
        }, f, indent=4)
    
    print(f"\n✅ Data for '{username}' has been saved to {username}_data.json")

if __name__ == "__main__":
    main()
