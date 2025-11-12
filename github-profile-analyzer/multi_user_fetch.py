# multi_user_fetch.py
from github_api import fetch_multiple_users
import json

def main():
    usernames = input("Enter GitHub usernames (comma-separated): ").split(',')
    usernames = [name.strip() for name in usernames]

    print("\nFetching data for multiple users...")
    all_data = fetch_multiple_users(usernames)

    # Save data to JSON file
    with open("multiple_users_data.json", "w") as f:
        json.dump(all_data, f, indent=4)

    print("\n✅ All users' data saved successfully in 'multiple_users_data.json'")

if __name__ == "__main__":
    main()
