// utilized chat to beak down some concepts 
// set up static variables
// used code from exam and hwk 4
const express = require("express");
const axios = require("axios");
const path = require("path");
const app = express();
const bodyParser = require('body-parser')


// set the view engine to ejs
app.set('view engine', 'ejs');

// route path to pages file within views
app.set('views', path.join(__dirname, 'views/pages'));

// static folder for public assets (CSS, JS, images)
app.use(express.static('./public'));

// body-parser middleware to handle form data
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public"))); // accesses static files in the public file

//API URL to Flask in sql.py
const API_URL = "http://127.0.0.1:5000"

// res.render to load home page
app.get('/', (req, res) => {
  res.render('index', {
    title: "Home Page",
    message: "Welcome to the Stock Brockerage System!"
  });
});

// index page to endpoint return one investor
// index page to endpoint add investor
// index page to endpoint edit investor
// index page to endpoint delete investor 
// index page to endpoint add stock
// index page to endpoint edit stock
// index page to endpoint delete stock
// index page to endpoint add bond
// index page to endpoint edit bond
// index page to endpoint delete bond
// index page to endpoint investor portfolio
// index page to endpoint stock transactions
// index page to endpoint bond transactions
// index page to endpoint to delete stock transactions
// index page to endpoint to delete bond transactions



// server is viewable on port 8080
app.listen(8080);
console.log(`Server is running on http://localhost:8080`);