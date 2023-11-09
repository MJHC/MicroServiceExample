const express = require('express');
const path = require('path');

const app = express();
const port = 8087; // You can change this to any port you prefer

// Define a middleware to serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Define a route to serve index.html at the root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Define a route to serve cake.html at /cake
app.get('/cake', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'cake.html'));
});

// Start the Express.js server
app.listen(port, () => {
  console.log(`Express.js app is running on http://localhost:${port}`);
});