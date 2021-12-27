const path = require('path');

const express = require('express');
const bodyParser = require('body-parser');

const PORT = 8080;

express()
  .use(bodyParser.json())
  .use(express.static(path.join(__dirname, 'dist')))
  .use('*', (req, res) => {
    res.sendFile('index.html', { root: path.join(__dirname, 'dist') });
  })
  .listen(PORT);
