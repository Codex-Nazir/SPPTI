import re

def check_email(email_text):
    score = 0
    reasons = []

    # Suspicious keywords
    keywords = ["urgent", "verify", "login", "bank", "update", "password"]

    for word in keywords:
        if word in email_text.lower():
            score += 1
            reasons.append(f"Suspicious keyword found: {word}")

    # Check for links
    links = re.findall(r'(https?://\S+)', email_text)
    if links:
        score += 1
        reasons.append("Email contains links")

    # Too many exclamation marks
    if email_text.count("!") > 3:
        score += 1
        reasons.append("Too many exclamation marks (urgency detected)")

    return score, reasons
