chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    let url = tabs[0].url;

    fetch("http://127.0.0.1:5000/check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url})
    })
    .then(res => res.json())
    .then(data => {
        let result = document.getElementById("result");

        if (data.risk_score >= 2) {
            result.innerText = "🔴 High Risk (Phishing)";
        } else if (data.risk_score == 1) {
            result.innerText = "⚠️ Suspicious";
        } else {
            result.innerText = "🟢 Safe";
        }
    });
});
