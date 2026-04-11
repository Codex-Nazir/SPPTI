from pyzbar.pyzbar import decode
from PIL import Image
import re

def analyze_qr(image_path):
    img = Image.open(image_path)
    decoded = decode(img)

    if not decoded:
        return {"error": "No QR code detected"}

    data = decoded[0].data.decode("utf-8")

    result = {
        "data": data,
        "type": "Unknown",
        "risk": "Low",
        "details": []
    }

    # 🔍 Detect URL
    if data.startswith("http"):
        result["type"] = "URL"
        
        if "@" in data or "login" in data or "verify" in data:
            result["risk"] = "High"
            result["details"].append("Suspicious URL detected")

    # 💳 Detect UPI Payment
    elif data.startswith("upi://"):
        result["type"] = "UPI Payment QR"

        if "paytm" in data:
            result["details"].append("Paytm QR")
        elif "phonepe" in data:
            result["details"].append("PhonePe QR")
        elif "gpay" in data:
            result["details"].append("Google Pay QR")

    # 📧 Email / text
    else:
        result["type"] = "Text/Data"

    return result
