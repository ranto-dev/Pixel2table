const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const captureBtn = document.getElementById("captureBtn");
const resultsBtn = document.getElementById("resultsBtn");
const indicators = document.getElementById("indicators");
const tablesContainer = document.getElementById("tablesContainer");
const numImagesInput = document.getElementById("numImages");
const loading = document.getElementById("loading");

let captureCount = 0;
let maxCaptures = parseInt(numImagesInput.value);

numImagesInput.onchange = () => {
  maxCaptures = parseInt(numImagesInput.value);
};

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (video.srcObject = stream));

captureBtn.onclick = async () => {
  if (captureCount >= maxCaptures) return;

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0);

  const image = canvas.toDataURL("image/jpeg");
  loading.hidden = false;

  const res = await fetch("http://localhost:8000/capture", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image }),
  });

  const data = await res.json();
  loading.hidden = true;

  if (data.error) {
    indicators.innerHTML = `⚠️ ${data.error}`;
    return;
  }

  captureCount = data.count;
  indicators.innerHTML = `✅ ${data.message}`;

  if (captureCount >= maxCaptures) {
    captureBtn.hidden = true;
    resultsBtn.hidden = false;
    indicators.innerHTML = "🎉 Toutes les images capturées !";
  }
};

resultsBtn.onclick = async () => {
  const res = await fetch("http://localhost:8000/results");
  const data = await res.json();

  tablesContainer.innerHTML = "";
  Object.keys(data).forEach((tableName) => {
    const rows = data[tableName];
    if (rows.length === 0) return;

    const table = document.createElement("table");
    const header = document.createElement("tr");
    [
      "ID",
      "Area",
      "Perimeter",
      "AspectRatio",
      "Solidity",
      "Circularity",
      "HuMoments",
      "Date",
    ].forEach((h) => {
      const th = document.createElement("th");
      th.innerText = h;
      header.appendChild(th);
    });
    table.appendChild(header);

    rows.forEach((row) => {
      const tr = document.createElement("tr");
      row.forEach((cell) => {
        const td = document.createElement("td");
        td.innerText = Array.isArray(cell)
          ? cell.map((v) => v.toFixed(2)).join(",")
          : cell;
        tr.appendChild(td);
      });
      table.appendChild(tr);
    });

    const title = document.createElement("h2");
    title.innerText = tableName.toUpperCase();
    tablesContainer.appendChild(title);
    tablesContainer.appendChild(table);
  });
};
