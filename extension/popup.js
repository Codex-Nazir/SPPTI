document.addEventListener("DOMContentLoaded", function () {

    // Get current tab URL automatically
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let currentUrl = tabs[0].url;

        document.getElementById("url").innerText = currentUrl;

        // Send to backend (Render URL)
        fetch("https://your-app-name.onrender.com/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: currentUrl })
        })
        .then(res => res.json())
        .then(data => {

            let result = document.getElementById("result");

            // Show score
            result.innerHTML = "Risk Score: " + data.risk_score;

            // Danger detection
            if (data.risk_score > 1) {
                result.style.color = "red";

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
                result.style.color = "green";
            }

        })
        .catch(err => {
            console.log("Error:", err);
        });

    });

});

