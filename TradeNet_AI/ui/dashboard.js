const BASE_URL = "http://192.168.0.101:5000"; // ⚠️ Use IP shown by Flask server

function generateSignals() {
  fetch(`${BASE_URL}/generate`)
    .then((res) => res.ok ? res.json() : Promise.reject("Server Error"))
    .then((data) => {
      document.getElementById("signal-output").innerHTML =
        `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch((err) => {
      document.getElementById("signal-output").innerText = "⚠️ Signal API Call Failed";
      console.error("Generate Error:", err);
    });
}

function checkStatus() {
  fetch(`${BASE_URL}/status`)
    .then((res) => res.ok ? res.json() : Promise.reject("Server Error"))
    .then((data) => {
      document.getElementById("booster-output").innerHTML =
        `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch((err) => {
      document.getElementById("booster-output").innerText = "⚠️ Status API Call Failed";
      console.error("Status Error:", err);
    });
}
