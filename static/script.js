const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const statusText = document.getElementById('status');
const fireMaskImg = document.getElementById('fireMask');
const alarm = document.getElementById('alarm');

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Webcam error:", err);
    statusText.textContent = "🚫 Could not access webcam.";
  });

// Send frame every 1 second
setInterval(() => {
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL('image/jpeg');

  fetch('/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageData })
  })
    .then(response => response.json())
    .then(data => {
      if (data.fire_detected) {
        statusText.innerHTML = "🔥 Fire Detected!";
        fireMaskImg.src = data.fire_mask;
        alarm.play();
      } else {
        statusText.innerHTML = "✅ No Fire Detected";
      }
    })
    .catch(err => {
      console.error("Detection error:", err);
    });
}, 1000);
