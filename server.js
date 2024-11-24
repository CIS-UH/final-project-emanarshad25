const express = require("express");
const axios = require("axios");
const path = require("path");
const app = express();
const bodyParser = require("body-parser");

// Set the view engine to EJS
app.set("view engine", "ejs");
// Route path to pages file within views
app.set("views", path.join(__dirname, "views/pages"));

// Static folder for public assets (CSS, JS, images)
app.use(express.static(path.join(__dirname, "public")));

// Middleware to handle form data
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// API Base URL for Flask server
const API_URL = "http://127.0.0.1:5000";

// ------------------------ Routes ------------------------

// Home Page
app.get("/", (req, res) => {
  res.render("index", {
    title: "Home Page",
    message: "Welcome to the Stock Brokerage System!",
  });
});

// Investor Portfolio Page
app.get("/investor/:id/portfolio", async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/portfolio`, {
      params: { investorID: req.params.id },
    });
    const portfolio = response.data;
    res.render("portfolio", { portfolio });
  } catch (error) {
    console.error("Error fetching portfolio:", error.message);
    res.status(500).send("Error fetching portfolio");
  }
});

// Stock Transactions Page
app.get("/stocktransactions", async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/stocktransactions`);
    const transactions = response.data;
    res.render("stocktransactions", { transactions });
  } catch (error) {
    console.error("Error fetching stock transactions:", error.message);
    res.status(500).send("Error fetching stock transactions");
  }
});

// Add Stock Transaction
app.post("/stocktransaction/add", async (req, res) => {
  try {
    const { investorid, stockid, quantity } = req.body;
    await axios.post(`${API_URL}/add_stocktransaction`, {
      investorid,
      stockid,
      quantity,
    });
    res.redirect("/stocktransactions");
  } catch (error) {
    console.error("Error adding stock transaction:", error.message);
    res.status(500).send("Error adding stock transaction");
  }
});

// Delete Stock Transaction
app.post("/stocktransaction/delete/:id", async (req, res) => {
  try {
    await axios.delete(`${API_URL}/delete_stocktransaction`, {
      data: { transactionID: req.params.id },
    });
    res.redirect("/stocktransactions");
  } catch (error) {
    console.error("Error deleting stock transaction:", error.message);
    res.status(500).send("Error deleting stock transaction");
  }
});

// Bond Transactions Page
app.get("/bondtransactions", async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/bondtransactions`);
    const transactions = response.data;
    res.render("bondtransactions", { transactions });
  } catch (error) {
    console.error("Error fetching bond transactions:", error.message);
    res.status(500).send("Error fetching bond transactions");
  }
});

// Add Bond Transaction
app.post("/bondtransaction/add", async (req, res) => {
  try {
    const { investorid, bondid, quantity } = req.body;
    await axios.post(`${API_URL}/add_bondtransaction`, {
      investorid,
      bondid,
      quantity,
    });
    res.redirect("/bondtransactions");
  } catch (error) {
    console.error("Error adding bond transaction:", error.message);
    res.status(500).send("Error adding bond transaction");
  }
});

// Delete Bond Transaction
app.post("/bondtransaction/delete/:id", async (req, res) => {
  try {
    await axios.delete(`${API_URL}/delete_bondtransaction`, {
      data: { transactionID: req.params.id },
    });
    res.redirect("/bondtransactions");
  } catch (error) {
    console.error("Error deleting bond transaction:", error.message);
    res.status(500).send("Error deleting bond transaction");
  }
});

// ------------------------ Investor Management ------------------------

// Add Investor
app.post("/investor", async (req, res) => {
  try {
    const { fname, lname } = req.body;
    await axios.post(`${API_URL}/add_investor`, { fname, lname });
    res.redirect("/");
  } catch (error) {
    console.error("Error adding investor:", error.message);
    res.status(500).send("Error adding investor");
  }
});

// Edit Investor
app.post("/investor/edit/:id", async (req, res) => {
  try {
    const { fname, lname } = req.body;
    await axios.put(`${API_URL}/edit_investor`, {
      ID: req.params.id,
      fname,
      lname,
    });
    res.redirect(`/investor/${req.params.id}/portfolio`);
  } catch (error) {
    console.error("Error editing investor:", error.message);
    res.status(500).send("Error editing investor");
  }
});

// Delete Investor
app.post("/investor/delete/:id", async (req, res) => {
  try {
    await axios.delete(`${API_URL}/delete_investor`, {
      data: { ID: req.params.id },
    });
    res.redirect("/");
  } catch (error) {
    console.error("Error deleting investor:", error.message);
    res.status(500).send("Error deleting investor");
  }
});

// ------------------------ Error Handling ------------------------

// 404 Page Not Found
app.use((req, res) => {
  res.status(404).send("404: Page not found");
});

// ------------------------ Start Server ------------------------

app.listen(8080, () => {
  console.log("Server is running on http://localhost:8080");
});
