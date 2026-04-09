import numpy as np
import re
import joblib

# Load trained model
model = joblib.load("model.pkl")

def has_ip(url):
    return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

# URL features
def extract_url_features(url):
    length = len(url)
    dots = url.count('.')
    https = 1 if url.startswith("https") else 0
    special_chars = url.count('@') + url.count('-') + url.count('_')
    ip = has_ip(url)
    subdomains = url.count('.') - 1

    return np.array([[length, dots, https, special_chars, ip, subdomains]])  # 2D for sklearn

# Email/text features
def extract_email_features(text):
    return np.array([[  # make 2D
        len(text),
        text.count("http"),
        text.count("urgent"),
        text.count("verify"),
        int("@" in text)
    ]])

def predict_url(url):
    features = extract_url_features(url)  # use URL features
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]  # confidence

    return prediction, round(probability * 100, 2)

def predict_email(text):
    features = extract_email_features(text)  # use email features
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return prediction, round(probability * 100, 2)

