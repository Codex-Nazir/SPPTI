document.addEventListener("DOMContentLoaded", function () {

    // Get current tab URL automatically
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let currentUrl = tabs[0].url;

        // Show current URL
        let urlDisplay = document.getElementById("url");
        urlDisplay.innerText = currentUrl;

        // Send to backend (Render URL)
        fetch("https://sppti.onrender.com/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: currentUrl })
        })
        .then(res => res.json()) // parse JSON
        .then(data => {          // ← use 'data' here

            let phishingResult = document.getElementById("phishing-result");
            let aiResult = document.getElementById("ai-result");

            // Show risk score
            phishingResult.innerText = "Risk Score: " + data.risk_score;

            // Show AI confidence if available
            if (data.ml_confidence !== undefined) {
                aiResult.innerText = "AI Confidence: " + data.ml_confidence + "%";
            }

            // Danger detection
            if (data.risk_score > 1) {
                phishingResult.style.color = "red";
                aiResult.style.color = "red";

                // ⚠️ ALERT
                alert("⚠️ Warning: This website may be phishing!");

                // 🔔 Chrome Notification
                chrome.notifications.create({
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "Security Alert",
                    message: "This website is potentially dangerous!"
                });

            } else {
                phishingResult.style.color = "green";
                aiResult.style.color = "green";
            }

        })
        .catch(err => {
            console.log("Error:", err);
        });

    });

});
