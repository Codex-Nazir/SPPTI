document.addEventListener("DOMContentLoaded", function () {
    // Get current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let currentUrl = tabs[0].url;
        document.getElementById("url").innerText = currentUrl;

        // Send to backend (Flask URL)
        fetch("https://sppti.onrender.com/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: currentUrl })
        })
        .then(res => res.json())
        .then(data => {
            let phishingResult = document.getElementById("phishing-result");
            let aiResult = document.getElementById("ai-result");

            if (data.error) {
                phishingResult.innerText = "Error: " + data.error;
                aiResult.innerText = "Error: " + data.error;
                phishingResult.style.color = "orange";
                aiResult.style.color = "orange";
                return;
            }

            // Show risk score
            phishingResult.innerText = "Risk Score: " + data.risk_score;

            // Show AI confidence
            aiResult.innerText = data.ml_confidence !== undefined ?
                "AI Confidence: " + data.ml_confidence + "%" :
                "AI Confidence: N/A";

            // Highlight phishing
            if (data.risk_score > 1) {
                phishingResult.style.color = "red";
                aiResult.style.color = "red";

                alert("⚠️ Warning: This website may be phishing!");

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


