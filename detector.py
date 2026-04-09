from ml_model import predict_url
import whois
import tldextract

def check_url(url):
    score = 0
    reasons = []

    # 1. Check HTTPS
    if not url.startswith("https"):
        score += 1
        reasons.append("URL is not using HTTPS")

    # 2. Suspicious keywords
    suspicious_words = ["login", "verify", "secure", "update", "bank"]
    if any(word in url.lower() for word in suspicious_words):
        score += 1
        reasons.append("Suspicious keywords in URL")

    # 3. Domain age
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix
        domain_info = whois.whois(domain)

        if domain_info.creation_date:
            score += 1
            reasons.append("Domain is recently registered")
    except:
        reasons.append("Could not verify domain info")

    # 4. ML detection ✅ (PROPERLY INSIDE FUNCTION)
    prediction, confidence = predict_url(url)

    if prediction == 1:
        score += 1
        reasons.append(f"ML detected phishing ({confidence}% confidence)")

    return score, reasons


if __name__ == "__main__":
    url = input("Enter URL: ")
    score, reasons = check_url(url)

    print("\nRisk Score:", score)
    print("Reasons:")
    for r in reasons:
        print("-", r)
