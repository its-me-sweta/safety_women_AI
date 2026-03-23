function sendSOS() {
  fetch('https://your-app.onrender.com/sos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: 'Help me!',
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById('status').innerText = data.status;
    });
}
