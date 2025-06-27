import re

def detect_input_type(value: str) -> str:
    if "," in value and all(re.match(r"[A-Z]+-\d+", v.strip()) for v in value.split(",")):
        return "ticket_list"
    elif re.match(r"^[A-Z]+-\d+$", value.strip()):
        return "ticket"
    elif "issues/?" in value and "jql=" in value:
        return "filter_url"
    else:
        return "unknown"