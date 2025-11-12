# data_extractor.py

def extract_repo_metrics(repos_data):
    """
    Extract key repository metrics like name, stars, forks, and language.
    """
    metrics = []
    for repo in repos_data:
        metrics.append({
            "name": repo.get("name"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", "N/A"),
            "updated": repo.get("updated_at", "N/A")
        })
    return metrics


def summarize_user_data(user_data):
    """
    Extract important user-level info like name, followers, and public repos.
    """
    if "error" in user_data:
        return user_data

    summary = {
        "name": user_data.get("name", "N/A"),
        "bio": user_data.get("bio", "N/A"),
        "public_repos": user_data.get("public_repos", 0),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "created_at": user_data.get("created_at", "N/A")
    }
    return summary
