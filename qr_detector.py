import cv2

def analyze_qr(image_path):
    img = cv2.imread(image_path)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if not data:
        return {"error": "No QR code detected"}

    result = {
        "data": data,
        "type": "Unknown",
        "risk": "Low",
        "details": []
    }

    # 🔍 URL detection
    if data.startswith("http"):
        result["type"] = "URL"

        if "@" in data or "login" in data or "verify" in data:
            result["risk"] = "High"
            result["details"].append("Suspicious URL detected")

    # 💳 UPI detection
    elif data.startswith("upi://"):
        result["type"] = "UPI Payment QR"

        if "paytm" in data:
            result["details"].append("Paytm QR")
        elif "phonepe" in data:
            result["details"].append("PhonePe QR")
        elif "gpay" in data:
            result["details"].append("Google Pay QR")

    else:
        result["type"] = "Text/Data"

    return result
