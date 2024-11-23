const express = require("express");
const axios = require("axios");
const path = require("path");
const app = express();
const bodyParser = require('body-parser');

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Define the views directory
app.set('views', path.join(__dirname, 'frontend/views/pages'));

// Define the static folder for public assets (CSS, JS, images)
app.use('/static', express.static(path.join(__dirname, 'frontend/public')));

// Body-parser middleware to handle form data
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// API URL to Flask backend
const API_URL = "http://127.0.0.1:5000";

// Render the home page
app.get('/', (req, res) => {
  res.render('index', {
    title: "Home Page",
    message: "Welcome to the Stock Brokerage System!"
  });
});

// Additional routes go here (e.g., for investors, stocks, bonds, transactions, etc.)

// Start the server
app.listen(8080, () => {
  console.log(`Server is running on http://localhost:8080`);
});
