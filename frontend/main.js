const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const captureBtn = document.getElementById("captureBtn");
const resultsBtn = document.getElementById("resultsBtn");
const output = document.getElementById("output");

let count = 0;

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (video.srcObject = stream));

captureBtn.onclick = async () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0);

  const image = canvas.toDataURL("image/jpeg");

  const res = await fetch("http://localhost:8000/capture", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image }),
  });

  const data = await res.json();
  count = data.count || count;

  if (count === 3) {
    captureBtn.hidden = true;
    resultsBtn.hidden = false;
  }
};

resultsBtn.onclick = async () => {
  const res = await fetch("http://localhost:8000/results");
  const data = await res.json();
  output.textContent = JSON.stringify(data, null, 2);
};
