1. View Investor's Current Portfolio (Stocks and Bonds)
This API retrieves all the stocks and bonds an investor currently holds by calculating the net quantity from the stocktransaction and bondtransaction tables.

API Endpoint: /api/investor_portfolio
Request:
URL: http://127.0.0.1:5000/api/investor_portfolio?investorid=1

2. Make a Stock Transaction (Buy or Sell a Stock)
URL: http://127.0.0.1:5000/api/stock_transaction
Body:
{
  "investorid": 1,
  "stockid": 1,
  "quantity": 10  # Positive for buy, negative for sell
}

Make a Bond Transaction
http://127.0.0.1:5000/api/bond_transaction
Body (JSON):
{
  "investorid": 1,
  "bondid": 1,
  "quantity": 5
}

3. Cancel a Stock Transaction (Delete a Stock Transaction)
http://127.0.0.1:5000/api/delete_stock_transaction
Body (JSON):
{
  "id": 1
}

