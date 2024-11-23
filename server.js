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
app.get("/investor/:id", async (req, res) => {
    //set constant that requires id to fetch possible existing investor
    try{
        const response = await axios.get(`${API_BASE_URL}/single_investor`, {
            data: {ID: req.params.id}
        });
        const investor = response.data[0];
        res.render("investor", {investor}); 
    } catch (error) {
        console.error("Error fetching investor:", error.message);
        res.status(500).send("Error fetching investor");
    }
});

// index page to endpoint add investor
app.post("/investor", async (req, res) => {
    try {
        const { fname, lname } = req.body;
        await axios.post(`${API_URL}/add_investor`, { fname, lname });
        res.redirect("/investors");
    } catch (error) {
        console.error("Error adding investor:", error.message);
        res.status(500).send("Error with adding investor");
    }
});

// index page to endpoint edit investor
app.post("/investor/edit/:id", async (req, res) => {
try {
    const {fname, lname} = req.body;
    await axios.put(`${API_URL}/edit_investor`, {
        ID: req.params.id,
        fname,
        lname
    });
    res.redirect(`/investor/${req.params.id}`);
} catch (error) {
    console.error("Error with editing investor:", error.message);
    res.status(500).send("Error with editing investor");
}
});

// index page to endpoint delete investor
app.post("/investor/delete/:id", async (req, res) => {
    try {
        await axios.delete(`${API_URL}/delete_investor`, {
            data: {ID: req.params.id}
        });
        res.redirect("/investors");
    } catch (error) {
        console.error("Error with deleting investor:", error.message);
        res.status(500).send("Error with deleting investor");
    }
});

// index page to endpoint add stock
app.post("/stock", async (req, res) => {
    try {
        const {stockname, abbreviation, currentprice} = req.body;
        await axios.post(`${API_URL}/add_stock`, {stockname, abbreviation, currentprice });
        res.redirect("/stocks");
    } catch (error) {
        console.error("Error with adding stock:", error.message);
        res.status(500).send("Error with adding stock");
    }
});

// index page to endpoint edit stock
app.post("/stock/edit/:id", async (req, res) => {
    try {
        const {stockname, abbreviation, currentprice} = req.body;
        await axios.post(`${API_URL}/edit_stock`, {
            ID: req.params.id,
            stockname,
            abbreviation,
            currentprice
        });
        res.redirect("/stocks");
    } catch (error) {
        console.error("Error with editing investor:", error.message);
        res.status(500).send("Error with adding investor");
    }
});
// index page to endpoint delete stock
app.post("/stock/delete/:id", async (req, res) => {
    try {
        await axios.delete(`${API_URL}/delete_stock`, {
            data: {ID: req.params.id}
        });
        res.redirect("/stocks");
    } catch (error) {
        console.error("Error with deleting investor:", error.message);
        res.status(500).send("Error with deleting investor");
    }
});

// index page to endpoint add bond
app.post("/bond", async (req, res) => {
    try {
        const {bondname, abbreviation, currentprice} = req.body;
        await axios.post(`${API_URL}/add_bond`, {bondname, abbreviation, currentprice });
        res.redirect("/bonds");
    } catch (error) {
        console.error("Error with adding bond:", error.message);
        res.status(500).send("Error with adding bond");
    }
});

// index page to endpoint edit bond
app.post("/bond/edit/:id", async (req, res) => {
    try {
        const {bondname, abbreviation, currentprice} = req.body;
        await axios.post(`${API_URL}/edit_stock`, {
            ID: req.params.id,
            bondname,
            abbreviation,
            currentprice
        });
        res.redirect("/bonds");
    } catch (error) {
        console.error("Error with editing bond:", error.message);
        res.status(500).send("Error with adding bond");
    }
});

// index page to endpoint delete bond
app.post("/bond/delete/:id", async (req, res) => {
    try {
        await axios.delete(`${API_URL}/delete_bond`, {
            data: {ID: req.params.id}
        });
        res.redirect("/bonds");
    } catch (error) {
        console.error("Error with deleting bond:", error.message);
        res.status(500).send("Error with deleting bond");
    }
});

// index page to endpoint investor portfolio
app.get("/investor/:id/portfolio", async (req, res) => {
  try {
      const response = await axios.get(`${API_URL}/portfolio`, {
          params: { investorID: req.params.id }
      });
      const portfolio = response.data;
      res.render("portfolio", { portfolio });
  } catch (error) {
      console.error("Error fetching portfolio:", error.message);
      res.status(500).send("Error fetching portfolio");
  }
});

// index page to endpoint stock transactions
app.post("/stocktransaction", async (req, res) => {
  try {
      const { investorid, stockid, quantity } = req.body;
      await axios.post(`${API_URL}/add_stocktransaction`, {
          investorid,
          stockid,
          quantity
      });
      res.redirect(`/investor/${investorid}/portfolio`);
  } catch (error) {
      console.error("Error adding stock transaction:", error.message);
      res.status(500).send("Error adding stock transaction");
  }
});

// index page to endpoint bond transactions
app.post("/bondtransaction", async (req, res) => {
  try {
      const { investorid, bondid, quantity } = req.body;
      await axios.post(`${API_URL}/add_bondtransaction`, {
          investorid,
          bondid,
          quantity
      });
      res.redirect(`/investor/${investorid}/portfolio`);
  } catch (error) {
      console.error("Error adding bond transaction:", error.message);
      res.status(500).send("Error adding bond transaction");
  }
});

// index page to endpoint to delete stock transactions
app.post("/stocktransaction/delete/:id", async (req, res) => {
  try {
      await axios.delete(`${API_URL}/delete_stocktransaction`, {
          data: { transactionID: req.params.id }
      });
      res.redirect("back");
  } catch (error) {
      console.error("Error deleting stock transaction:", error.message);
      res.status(500).send("Error deleting stock transaction");
  }
});

// index page to endpoint to delete bond transactions
app.post("/bondtransaction/delete/:id", async (req, res) => {
  try {
      await axios.delete(`${API_URL}/delete_bondtransaction`, {
          data: { transactionID: req.params.id }
      });
      res.redirect("back");
  } catch (error) {
      console.error("Error deleting bond transaction:", error.message);
      res.status(500).send("Error deleting bond transaction");
  }
});


// server is viewable on port 8080
app.listen(8080);
console.log(`Server is running on http://localhost:8080`);