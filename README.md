

# Jira BDD Test Case Generator

This project automates the generation of Gherkin-style BDD test cases directly from Jira issues using OpenAI.

## 🔧 Features

- ✅ Supports single Jira tickets, comma-separated ticket lists, and filter URLs.
- ✅ AI-enhanced test case generation using GPT-4o.
- ✅ Auto-detection of story types (Epic, Story, etc.).
- ✅ One `.feature` file is generated per story with contextual naming.
- ✅ Prompts user interactively when no input is provided via CLI.

## 📂 Output

- Each Jira ticket creates a standalone `.feature` file under `output/`
- Files are named based on the story summary and Jira issue number (e.g., `profile_header_redesign_36.feature`)

## 🚀 Usage

Run the tool from your terminal:

```bash
python3 main.py
```

You'll be prompted to enter:
- A single ticket ID: `SCRUM-36`
- Multiple ticket IDs: `SCRUM-36,SCRUM-40,SCRUM-42`
- A Jira filter URL: `https://your-domain.atlassian.net/issues/?jql=...`

## 🧠 AI Behavior

The model:
- Picks appropriate Gherkin keywords from the full set: `Feature`, `Rule`, `Background`, `Scenario`, `Scenario Outline`, `Given`, `When`, `Then`, `And`, `But`, `*`
- Builds test cases based on Jira Summary, Business Rules, and Acceptance Criteria.
- Decides the "Feature" name dynamically based on the content of each Jira story.

## 🔐 Requirements

- Python 3.8+
- `openai` Python package (v1.0+)
- A valid `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_key
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_jira_token
PROJECT_KEY=your_project_key
```

## 📁 File Structure

```
📁 output/               # Generated .feature files
📄 main.py               # Entry point for the script
📄 jira_utils.py         # Jira API interaction logic
📄 bdd_generator.py      # AI logic for BDD test generation
📄 .env                  # Local environment variables
```

## 🛠️ Future Enhancements

- Support for uploading `.feature` files to Zephyr Scale automatically.
- Confluence export of generated documentation.
- Option to merge multiple stories into one combined `.feature`.

## 🧪 Sample

Example output snippet:

```gherkin
Feature: Profile Header Redesign

  Scenario: Ensure header layout renders for mobile
    Given I am on the profile page
    When I view the page on a mobile device
    Then I should see the redesigned header with full metadata
```

---