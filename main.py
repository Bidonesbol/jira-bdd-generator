from utils import detect_input_type
from jira_client import fetch_issue, fetch_issues_from_filter_url, fetch_children_for_epic
from bdd_generator import generate_features
import sys

def is_epic(issue_data):
    issue_type = issue_data.get("fields", {}).get("issuetype", {}).get("name", "")
    return issue_type.lower() == "epic"

def print_issue_summary(issue):
    key = issue.get("key")
    summary = issue.get("fields", {}).get("summary", "")
    print(f"- [{key}] {summary}")

def main():
    input_value = input("🔹 Enter a Jira Story ID, Epic ID, Filter URL, or comma-separated list of IDs: ").strip()
    if not input_value:
        print("❌ No input provided. Exiting.")
        sys.exit(1)

    user_input = input_value
    input_type = detect_input_type(user_input)

    print(f"\n✅ Input received: {user_input}")
    print(f"🔍 Detected input type: {input_type}")

    if input_type == "ticket":
        issue = fetch_issue(user_input)
        if is_epic(issue):
            print(f"📘 {user_input} is an Epic. Fetching child stories...")
            children = fetch_children_for_epic(user_input)
            if not children:
                print("⚠️ No child issues found.")
            else:
                print(f"\n✅ Found {len(children)} child issue(s):")
                for child in children:
                    print_issue_summary(child)
                generate_features(children)
        else:
            print(f"📄 {user_input} is not an Epic.")
            print_issue_summary(issue)
            generate_features([issue])

    elif input_type == "ticket_list":
        ticket_ids = [tid.strip() for tid in user_input.split(",")]
        issues = [fetch_issue(tid) for tid in ticket_ids]
        for issue in issues:
            print_issue_summary(issue)
        generate_features(issues)

    elif input_type == "filter_url":
        issues = fetch_issues_from_filter_url(user_input)
        print(f"📦 Retrieved {len(issues)} issues:")
        for issue in issues:
            print_issue_summary(issue)
        generate_features(issues)

    else:
        print("❌ Unsupported input type.")

if __name__ == "__main__":
    main()