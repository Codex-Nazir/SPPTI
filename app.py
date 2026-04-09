from email_detector import check_email
from database import save_scan, get_all_scans
from flask import Flask, request, jsonify, render_template
from detector import check_url

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    url = data.get("url")

    score, reasons = check_url(url)

    save_scan(url, score, reasons)

    return jsonify({
        "url": url,
        "risk_score": score,
        "reasons": reasons
    })

# ✅ ADD THIS PART
@app.route("/history")
def history():
    data = get_all_scans()
    return render_template("history.html", data=data)

@app.route("/check_email", methods=["POST"])
def check_email_route():
    data = request.json
    email_text = data.get("email")

    score, reasons = check_email(email_text)

    return jsonify({
        "risk_score": score,
        "reasons": reasons
    })

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




