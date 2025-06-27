import os
import re
import unicodedata
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sanitize_filename(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '_', text)
    return text

def extract_numeric_key(key):
    match = re.search(r'(\d+)$', key)
    return match.group(1) if match else key

def generate_bdd_from_issue(issue):
    key = issue.get("key", "UNKNOWN")
    fields = issue.get("fields", {})
    summary = fields.get("summary", "").strip()
    description = fields.get("description", "").strip()
    acceptance_criteria = fields.get("customfield_10045", "")

    prompt = f"""Given the following Jira story, generate complete Gherkin-style BDD test cases.

- Use all applicable Gherkin keywords when appropriate (Feature, Rule, Background, Scenario, Scenario Outline, Given, When, Then, And, But, '*').
- Do not include markdown formatting like triple backticks (` ``` `) or any other non-Gherkin syntax.
- Start with the Feature declaration, based on the content of the story (not the script’s purpose).
- Include relevant tags (e.g. @{key.replace("-", "")}).
- Generate as many relevant scenarios as needed based on the story scope.

Summary: {summary}
Description: {description}
Acceptance Criteria: {acceptance_criteria}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior QA engineer who writes comprehensive BDD test cases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ AI generation failed for {key}: {e}")
        return f"""Feature: {summary or "Untitled"}
  Scenario: Placeholder for {key}
    Given some context
    When an action is performed
    Then an expected result occurs
"""

def generate_features(issues, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    for issue in issues:
        key = issue.get("key", "UNKNOWN")
        fields = issue.get("fields", {})
        summary = fields.get("summary", "story").strip()
        numeric_key = extract_numeric_key(key)
        file_safe_summary = sanitize_filename(summary or "story")
        filename = f"{file_safe_summary}_{numeric_key}.feature"
        filepath = os.path.join(output_dir, filename)

        bdd_text = generate_bdd_from_issue(issue)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(bdd_text + "\n")

        print(f"✅ Feature file generated for {key}: {filepath}")