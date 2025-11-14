import os
import json
import pandas as pd

def load_raw_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def json_to_dfs(data):
    profile_data = data.get("profile", {})
    repos_data = data.get("repos", [])

    profile_df = pd.DataFrame([profile_data])
    repos_df = pd.DataFrame(repos_data)

    return profile_df, repos_df

def clean_repos_df(df):
    df["stargazers_count"] = df["stargazers_count"].fillna(0)
    df["language"] = df["language"].fillna("Unknown")
    return df

def build_summary(profile_df, repos_df):
    summary = {
        "profile": {
            "login": profile_df["login"].iloc[0],
            "public_repos": profile_df["public_repos"].iloc[0],
            "followers": profile_df["followers"].iloc[0],
            "following": profile_df["following"].iloc[0],
        },
        "repos_count": len(repos_df),
        "repos_by_language": repos_df["language"].value_counts().to_dict(),
        "top_repos_by_stars": repos_df.nlargest(5, "stargazers_count")[["name", "stargazers_count"]].to_dict(orient="records")
    }
    return summary

if _name_ == "_main_":
    raw_data = load_raw_json("sample_raw.json")
    profile_df, repos_df = json_to_dfs(raw_data)
    repos_df = clean_repos_df(repos_df)

    summary = build_summary(profile_df, repos_df)

    print(json.dumps(summary, indent=2))

    # Save processed data into JSON file
    with open("processed_data.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print("processed_data.json created successfully 🎉")