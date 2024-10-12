# Eman Arshad ID: 2048488

# Amelie's Part 
import flask
from flask import jsonify, request
import mysql.connector
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query

# Setting up an application name
app = flask.Flask(__name__)  # sets up application
app.config["DEBUG"] = True  # allows showing errors in the browser

# Eman's Credentials 
conn = create_connection("cis2368fall.c7kgkamim5gh.us-east-1.rds.amazonaws.com", "admin", "Emaan200325", "cis2368falldb")
cursor = conn.cursor(dictionary=True)

sql = "SELECT * FROM investor"
cursor.execute(sql)
investor_tb = cursor.fetchall()

sql2 = "SELECT * FROM stock"
cursor.execute(sql2)
stock_tb = cursor.fetchall()

sql3 = "SELECT * FROM bond"
cursor.execute(sql3)
bond_tb = cursor.fetchall()

# Get all investors
@app.route('/api/investor', methods=['GET'])
def api_get_all_investors():
    call_investor = "SELECT * FROM investor"
    investor_list = execute_read_query(conn, call_investor)
    return jsonify(investor_list)

# Get one investor by ID
@app.route('/api/single_investor', methods=['GET'])
def api_get_single_investor():
    request_data = request.get_json()
    fetch_id = request_data["id"]
    for i in range(len(investor_tb)):
        if investor_tb[i]['ID'] == fetch_id:
            query = f"SELECT * FROM investor WHERE id = {fetch_id}"
            result = execute_read_query(conn, query)
            return jsonify(result)
    return "No match found"

# Add an investor
@app.route('/api/add_investor', methods=['POST'])
def api_add_investor():
    request_data = request.get_json()
    new_fname = request_data["firstname"]
    new_lname = request_data["lastname"]
    query = f"INSERT INTO investor (firstname, lastname) VALUES ('{new_fname}','{new_lname}')"
    execute_query(conn, query) 
    return "Investor added successfully"

# Edit an investor
@app.route('/api/investor_edit', methods=['PUT'])
def api_edit_investor():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newfname = request_data["firstname"]
    newlname = request_data["lastname"]
    query = f"UPDATE investor SET firstname = '{newfname}', lastname = '{newlname}' WHERE id = {idToUpdate}"
    execute_query(conn, query)
    return "Investor updated successfully"

# Delete an investor
@app.route('/api/delete_investor', methods=['DELETE'])
def api_delete_investor():
    request_data = request.get_json()
    idToDelete = request_data['id']
    query = f"DELETE FROM investor WHERE ID = {idToDelete}"
    execute_query(conn, query)
    return "Investor deleted successfully"

# Add stock
@app.route('/api/addstock', methods=['POST'])
def api_add_stock():
    request_data = request.get_json()
    new_stockname = request_data['stockname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = f"INSERT INTO stock (stockname, abbreviation, currentprice) VALUES ('{new_stockname}','{new_abbr}', {new_price})"
    execute_query(conn, query)
    return "Stock added successfully"

# Edit stock
@app.route('/api/edit_stock', methods=['PUT'])
def api_edit_stock():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newsname = request_data["stockname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    query = f"UPDATE stock SET stockname = '{newsname}', abbreviation = '{newabb}', currentprice = {newprice} WHERE id = {idToUpdate}"
    execute_query(conn, query)
    return "Stock updated successfully"

# Delete stock
@app.route('/api/delete_stock', methods=['DELETE'])
def api_delete_stock():
    request_data = request.get_json()
    idToDelete = request_data['id']
    query = f"DELETE FROM stock WHERE ID = {idToDelete}"
    execute_query(conn, query)
    return "Stock deleted successfully"

# Add bond
@app.route('/api/add_bond', methods=['POST'])
def api_add_bond():
    request_data = request.get_json()
    new_bondname = request_data['bondname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = f"INSERT INTO bond (bondname, abbreviation, currentprice) VALUES ('{new_bondname}','{new_abbr}', {new_price})"
    execute_query(conn, query)
    return "Bond added successfully"

# Edit bond
@app.route('/api/edit_bond', methods=['PUT'])
def api_edit_bond():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newbname = request_data["bondname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    query = f"UPDATE bond SET bondname = '{newbname}', abbreviation = '{newabb}', currentprice = {newprice} WHERE id = {idToUpdate}"
    execute_query(conn, query)
    return "Bond updated successfully"

# Delete bond
@app.route('/api/delete_bond', methods=['DELETE'])
def api_delete_bond():
    request_data = request.get_json()
    idToDelete = request_data['id']
    query = f"DELETE FROM bond WHERE ID = {idToDelete}"
    execute_query(conn, query)
    return "Bond deleted successfully"

# Investor Portfolio (Stocks and Bonds)
@app.route('/api/investor_portfolio', methods=['GET'])
def api_investor_portfolio():
    request_data = request.get_json()
    investor_id = request_data['investorid']

    stock_query = f"SELECT s.stockname, st.quantity FROM stocktransaction st JOIN stock s ON st.stockid = s.id WHERE st.investorid = {investor_id}"
    stock_portfolio = execute_read_query(conn, stock_query)

    bond_query = f"SELECT b.bondname, bt.quantity FROM bondtransaction bt JOIN bond b ON bt.bondid = b.id WHERE bt.investorid = {investor_id}"
    bond_portfolio = execute_read_query(conn, bond_query)

    return jsonify({'stocks': stock_portfolio, 'bonds': bond_portfolio})

# Stock Transaction (Buy/Sell)
@app.route('/api/stock_transaction', methods=['POST'])
def api_stock_transaction():
    request_data = request.get_json()
    investor_id = request_data['investorid']
    stock_id = request_data['stockid']
    quantity = request_data['quantity']  # Positive for buy, negative for sell

    current_query = f"SELECT SUM(quantity) AS total_quantity FROM stocktransaction WHERE investorid = {investor_id} AND stockid = {stock_id}"
    current_quantity = execute_read_query(conn, current_query)[0]['total_quantity'] or 0

    if quantity < 0 and abs(quantity) > current_quantity:
        return "Sale exceeds current holdings", 400

    query = f"INSERT INTO stocktransaction (investorid, stockid, quantity, date) VALUES ({investor_id}, {stock_id}, {quantity}, NOW())"
    execute_query(conn, query)
    return "Stock transaction successful"

# Bond Transaction (Buy/Sell)
@app.route('/api/bond_transaction', methods=['POST'])
def api_bond_transaction():
    request_data = request.get_json()
    investor_id = request_data['investorid']
    bond_id = request_data['bondid']
    quantity = request_data['quantity']  # Positive for buy, negative for sell

    current_query = f"SELECT SUM(quantity) AS total_quantity FROM bondtransaction WHERE investorid = {investor_id} AND bondid = {bond_id}"
    current_quantity = execute_read_query(conn, current_query)[0]['total_quantity'] or 0

    if quantity < 0 and abs(quantity) > current_quantity:
        return "Sale exceeds current holdings", 400

    query = f"INSERT INTO bondtransaction (investorid, bondid, quantity, date) VALUES ({investor_id}, {bond_id}, {quantity}, NOW())"
    execute_query(conn, query)
    return "Bond transaction successful"

# Delete Stock Transaction
@app.route('/api/delete_stock_transaction', methods=['DELETE'])
def api_delete_stock_transaction():
    request_data = request.get_json()
    transaction_id = request_data['id']
    query = f"DELETE FROM stocktransaction WHERE id = {transaction_id}"
    execute_query(conn, query)
    return "Stock transaction deleted successfully"

# Delete Bond Transaction
@app.route('/api/delete_bond_transaction', methods=['DELETE'])
def api_delete_bond_transaction():
    request_data = request.get_json()
    transaction_id = request_data['id']
    query = f"DELETE FROM bondtransaction WHERE id = {transaction_id}"
    execute_query(conn, query)
    return "Bond transaction deleted successfully"

if __name__ == '__main__':        
    app.run()