from ml_model import predict_url
from datetime import datetime
import whois
import tldextract
import re
import requests

def check_url(url):
    score = 0
    reasons = []

    # 1. HTTPS check (basic for now)
    if not url.startswith("https"):
        score += 1
        reasons.append("URL is not using HTTPS")

    # 2. Suspicious keywords
    suspicious_words = ["login", "verify", "secure", "update", "bank"]
    if any(word in url.lower() for word in suspicious_words):
        score += 1
        reasons.append("Suspicious keywords in URL")

    # 3. URL length
    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long")

    # 4. Too many subdomains
    if url.count('.') > 5:
        score += 1
        reasons.append("Too many subdomains")

    # 5. Suspicious symbols
    if "@" in url or "//" in url[8:]:
        score += 2
        reasons.append("Suspicious URL structure")

    # 6. IP address detection
    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        score += 2
        reasons.append("IP address used instead of domain")

    # 7. Domain age check
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix
        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            age_days = (datetime.now() - creation_date).days

            if age_days < 30:
                score += 2
                reasons.append("Domain is very new (<30 days)")
            elif age_days < 180:
                score += 1
                reasons.append("Domain is relatively new")

    except:
        reasons.append("Could not verify domain age")

    # 8. ML detection
    prediction, confidence = predict_url(url)

    if prediction == 1:
        score += 2
        reasons.append(f"ML detected phishing ({confidence}% confidence)")

    # 9. Final return
    return score, confidence, reasons
