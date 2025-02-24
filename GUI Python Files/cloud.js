const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 5002; // You can choose any available port

app.get('/get-csv', (req, res) => {
  const filePath = path.join(__dirname, 'data.csv'); // Replace 'data.csv' with your CSV file name
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(404).send('File not found');
    }
    res.send(data);
  });
});

app.listen(port, () => {
  console.log(`Cloud Server running at http://192.168.1.35:${port}`);
});
