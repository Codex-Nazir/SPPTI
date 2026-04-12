from PIL import Image
from PyPDF2 import PdfReader
import os

def analyze_file(file_path):
    result = {
        "type": "Unknown",
        "risk": "Low",
        "details": []
    }

    # 📷 IMAGE ANALYSIS
    if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        result["type"] = "Image"

        try:
            img = Image.open(file_path)
            metadata = img.info

            if metadata:
                result["details"].append("Metadata found in image")

                # suspicious if too much metadata
                if len(metadata) > 5:
                    result["risk"] = "Medium"
                    result["details"].append("Too much hidden metadata")

            else:
                result["details"].append("No metadata found")

        except:
            result["risk"] = "Medium"
            result["details"].append("Error reading image")

    # 📄 PDF ANALYSIS
    elif file_path.lower().endswith(".pdf"):
        result["type"] = "PDF"

        try:
            reader = PdfReader(file_path)

            # metadata
            meta = reader.metadata
            if meta:
                result["details"].append("PDF metadata found")

            # check text for suspicious words
            for page in reader.pages:
                text = page.extract_text()

                if text:
                    if "http" in text or "login" in text or "verify" in text:
                        result["risk"] = "High"
                        result["details"].append("Suspicious links/text found")

        except:
            result["risk"] = "High"
            result["details"].append("Corrupted or malicious PDF")

    else:
        result["details"].append("Unsupported file type")

    return result

