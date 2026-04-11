import re

def check_email(text):
    score = 0
    reasons = []

    text_lower = text.lower()

    # Suspicious keywords
    keywords = ["urgent", "verify", "account", "password", "bank", "login"]
    for word in keywords:
        if word in text_lower:
            score += 1
            reasons.append(f"Contains suspicious word: {word}")

    # Links in email
    if "http" in text_lower:
        score += 1
        reasons.append("Contains link")

    # Urgency phrases
    if "immediately" in text_lower or "action required" in text_lower:
        score += 1
        reasons.append("Creates urgency")

    # Fake sender pattern
    if "@" in text and "." not in text.split("@")[-1]:
        score += 1
        reasons.append("Suspicious email format")

    # Final classification
    if score >= 3:
        reasons.append("🚨 High Risk (Phishing)")
    elif score == 2:
        reasons.append("⚠️ Medium Risk")
    else:
        reasons.append("✅ Likely Safe")

    return score, reasons


