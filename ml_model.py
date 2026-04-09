import numpy as np
import re
import joblib

# Load trained model
model = joblib.load("model.pkl")


def has_ip(url):
    return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0


def extract_features(url):
    length = len(url)
    dots = url.count('.')
    https = 1 if url.startswith("https") else 0
    special_chars = url.count('@') + url.count('-') + url.count('_')
    ip = has_ip(url)
    subdomains = url.count('.') - 1

    return np.array([[length, dots, https, special_chars, ip, subdomains]])

def extract_features(text):
    return [
        len(text),
        text.count("http"),
        text.count("urgent"),
        text.count("verify"),
        int("@" in text)
    ]

def predict_url(url):
    features = extract_features(url)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]  # confidence

    return prediction, round(probability * 100, 2)
