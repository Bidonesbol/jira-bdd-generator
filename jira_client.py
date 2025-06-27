import os
import requests
from urllib.parse import unquote, urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def fetch_issue(issue_id):
    url = f"{JIRA_URL}/rest/api/2/issue/{issue_id}"
    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json()

def fetch_issues_from_filter_url(filter_url):
    parsed = urlparse(filter_url)
    query_params = parse_qs(parsed.query)
    raw_jql = query_params.get("jql", [""])[0]
    decoded_jql = unquote(raw_jql)

    url = f"{JIRA_URL}/rest/api/2/search"
    params = {"jql": decoded_jql, "maxResults": 50}  # Adjust maxResults if needed
    response = requests.get(url, headers=headers, auth=auth, params=params)
    response.raise_for_status()
    return response.json().get("issues", [])

def fetch_children_for_epic(epic_key):
    # First try with "Epic Link" (used in classic projects)
    try:
        jql = f'"Epic Link" = {epic_key}'
        url = f"{JIRA_URL}/rest/api/2/search"
        params = {"jql": jql, "maxResults": 50}
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        print("✅ Retrieved children using 'Epic Link'")
        return response.json().get("issues", [])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("⚠️ 'Epic Link' query failed. Trying 'parent' field...")
            try:
                jql = f'parent = {epic_key}'
                params = {"jql": jql, "maxResults": 50}
                response = requests.get(url, headers=headers, auth=auth, params=params)
                response.raise_for_status()
                print("✅ Retrieved children using 'parent'")
                return response.json().get("issues", [])
            except Exception as fallback_error:
                print(f"❌ Failed fallback query using 'parent': {fallback_error}")
                return []
        else:
            raise