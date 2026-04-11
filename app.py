from qr_detector import analyze_qr
from ml_model import predict_url
from flask import Flask, request, jsonify, render_template
from email_detector import check_email
from database import save_scan, get_all_scans
from detector import check_url

app = Flask(__name__)

# ----------------------------
# Full manual CORS handling
# ----------------------------
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # allow any origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/scan_qr", methods=["POST"])
def scan_qr():
    file = request.files["file"]
    
    filepath = "temp_qr.png"
    file.save(filepath)

    result = analyze_qr(filepath)

    return jsonify(result)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    url = data.get("url")

    try:
        # Use detector.py's check_url to get score, confidence, reasons
        score, ml_confidence, reasons = check_url(url)

        save_scan(url, score, reasons)

        return jsonify({
            "url": url,
            "risk_score": score,
            "ml_confidence": ml_confidence,  # ✅ ML confidence
            "reasons": reasons
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/check_email", methods=["POST", "OPTIONS"])
def check_email_route():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return add_cors_headers(response)

    data = request.json
    email_text = data.get("email")
    score, reasons = check_email(email_text)

    return jsonify({
        "risk_score": score,
        "reasons": reasons
    })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    data = get_all_scans()
    return render_template("history.html", data=data)

@app.route("/dashboard")
def dashboard():
    data = get_all_scans()
    total = len(data)
    high = sum(1 for d in data if d[2] >= 2)
    medium = sum(1 for d in data if d[2] == 1)
    low = sum(1 for d in data if d[2] == 0)
    return render_template("dashboard.html",
                           total=total,
                           high=high,
                           medium=medium,
                           low=low)

if __name__ == "__main__":
    app.run(debug=True)
