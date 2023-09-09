const express = require('express');
const app = express();
const port = 3000;

// Middleware to capture x-host header
app.use((req, res, next) => {
  req.xhost = req.headers['x-host'] || 'unknown';
  next();
});

// Your existing route
app.get('/', (req, res) => {
  const clientIp = req.connection.remoteAddress;
  const targetHost = req.xhost;

  res.send(`Hello user, you came from host IP: ${clientIp} and your target is ${targetHost}`);
});

// Route for the liveness probe
app.get('/health', (req, res) => {
  res.sendStatus(200);
});

// Route for the readiness probe
app.get('/ready', (req, res) => {
  res.sendStatus(200);
});

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
