import json
import pandas as pd

def load_raw_json(path):
    """Loads and shows the GitHub data from your JSON file"""
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def json_to_dfs(raw):
    """Turns JSON into two DataFrames: profile_df and repos_df"""
    profile = raw.get('profile', {})
    repos = raw.get('repos', [])

    # Create profile table (1 row)
    profile_df = pd.DataFrame([{
        'login': profile.get('login'),
        'name': profile.get('name'),
        'followers': profile.get('followers'),
        'following': profile.get('following'),
        'public_repos': profile.get('public_repos'),
        'created_at': profile.get('created_at')
    }])
    repos_df = pd.DataFrame(repos)

    return profile_df, repos_df


    # Create repo table (multiple rows)
 
def clean_repos_df(repos_df):
    """Clean and fix missing or incorrect data in the repos DataFrame"""
    # Convert date columns to proper datetime format
    date_columns = ['created_at', 'updated_at', 'pushed_at']
    for col in date_columns:
        repos_df[col] = pd.to_datetime(repos_df[col], errors='coerce')

    # Replace missing languages with 'Unknown'
    repos_df['language'] = repos_df['language'].fillna('Unknown')

    # Make sure numeric columns are integers (no decimals)
    numeric_cols = ['stargazers_count', 'forks_count', 'watchers_count', 'size']
    for col in numeric_cols:
        if col in repos_df.columns:
            repos_df[col] = repos_df[col].fillna(0).astype(int)

    return repos_df

# ----------------------------
# Analysis / summary helpers
# ----------------------------
def total_stars(repos_df):
    """Return total stargazers across all repos (int)."""
    if repos_df is None or repos_df.empty:
        return 0
    return int(repos_df['stargazers_count'].sum())

def top_repos_by_stars(repos_df, n=5):
    """Return top n repos (DataFrame) sorted by stars."""
    if repos_df is None or repos_df.empty:
        return repos_df.head(0)
    return repos_df.sort_values('stargazers_count', ascending=False).head(n)[
        ['name', 'stargazers_count', 'language', 'forks_count', 'watchers_count']
    ]

def top_languages(repos_df, n=6):
    """Return a dict of top n languages and their repo counts."""
    if repos_df is None or repos_df.empty:
        return {}
    return repos_df['language'].value_counts().head(n).to_dict()

def avg_stars_per_repo(repos_df):
    """Return average stars per repo (float)."""
    if repos_df is None or repos_df.empty:
        return 0.0
    return float(repos_df['stargazers_count'].mean())

def commits_by_month(repos_df):
    """Count last push per repo grouped by month 'YYYY-MM' -> count."""
    if repos_df is None or repos_df.empty:
        return {}
    df = repos_df.dropna(subset=['pushed_at']).copy()
    if df.empty:
        return {}
    df['month'] = df['pushed_at'].dt.to_period('M').astype(str)
    series = df['month'].value_counts().sort_index()
    return series.to_dict()
def build_summary(profile_df, repos_df):
    """Bundle all analysis results into one clean dictionary for UI/visuals."""
    summary = {
        "profile": {
            "login": profile_df.iloc[0]['login'],
            "name": profile_df.iloc[0]['name'],
            "followers": int(profile_df.iloc[0]['followers']),
            "following": int(profile_df.iloc[0]['following']),
            "public_repos": int(profile_df.iloc[0]['public_repos']),
            "created_at": profile_df.iloc[0]['created_at']
        },
        "totals": {
            "total_repos": len(repos_df),
            "total_stars": total_stars(repos_df),
            "avg_stars_per_repo": round(avg_stars_per_repo(repos_df), 2)
        },
        "top_languages": top_languages(repos_df),
        "top_repos": top_repos_by_stars(repos_df, n=5).to_dict(orient="records"),
        "commits_by_month": commits_by_month(repos_df)
    }
    return summary

if __name__ == "__main__":
    raw_data = load_raw_json("sample_raw.json")
    profile_df, repos_df = json_to_dfs(raw_data)
    repos_df = clean_repos_df(repos_df)

    summary = build_summary(profile_df, repos_df)
    import json
    print(json.dumps(summary, indent=2))