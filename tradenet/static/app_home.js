// app_home.js
document.addEventListener("DOMContentLoaded", async () => {
  const tableBody = document.querySelector("#signal-table tbody");

  // Fetch signal data from backend
  const res = await fetch("/generate");
  const data = await res.json();

  // Render each row
  data.forEach((signal) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${signal.symbol}</td>
      <td>${signal.signal}</td>
      <td>${signal.confidence}</td>
      <td>${signal.booster}</td>
      <td>${signal.time}</td>
    `;

    // Redirect when row clicked
    row.addEventListener("click", () => {
      window.location.href = `/signal/${signal.symbol}`;
    });

    tableBody.appendChild(row);
  });
});
