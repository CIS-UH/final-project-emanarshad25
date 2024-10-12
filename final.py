# Eman Arshad ID: 2048488
import flask
from flask import jsonify
from flask import request
import mysql.connector
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up application
app.config["DEBUG"] = True #allows to show errors in browser

conn = create_connection("cis2368fall.c7kgkamim5gh.us-east-1.rds.amazonaws.com", "admin", "Emaan200325", "cis2368falldb")
cursor = conn.cursor(dictionary = True)

sql = "SELECT * FROM investor"
cursor.execute(sql)
investor_tb = cursor.fetchall()

sql2 = "SELECT * from stock"
cursor.execute(sql2)
stock_tb = cursor.fetchall()

sql3 = "SELECT * from bond"
cursor.execute(sql3)
bond_tb = cursor.fetchall()

@app.route('/api/investor', methods=['GET'])
def api_all():
    call_investor = "SELECT * FROM investor"
    investor_list = execute_read_query(conn, call_investor)
    return jsonify(investor_list)

#returns one investor from ID
@app.route('/api/single_investor', methods=['GET'])
def api_id():
    request_data = request.get_json()
    fetch_id = request_data["id"]
    for i in range(len(investor_tb)):
        if investor_tb[i]['ID'] == fetch_id:
            query = f"""SELECT * FROM investor 
            WHERE id = {fetch_id} """
            result = execute_read_query(conn, query)
            return jsonify(result)
    return "no match found"

# add users
@app.route('/api/add_investor', methods =['POST'])
def api_add():
    request_data = request.get_json()
    new_fname = request_data["firstname"]
    new_lname = request_data["lastname"]
    query = """INSERT INTO investor (firstname, lastname)
    VALUES ('%s','%s');""" %(new_fname, new_lname)
    execute_query(conn, query) 
    return "add request successful"

#edit users - edits all values code similar to homework 2 extra credit
@app.route('/api/investor_edit', methods=['PUT'])
def api_update_all():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newfname = request_data["firstname"]
    newlname = request_data["lastname"]
    for i in range(len(investor_tb)):
        if investor_tb[i]['ID'] == idToUpdate:
            query = """UPDATE investor 
            SET firstname = '%s', lastname = '%s' 
            WHERE id = %s""" %(newfname, newlname, idToUpdate)
            execute_query(conn,query)

#deletes user
@app.route('/api/delete_investor', methods=['DELETE'])
def api_delete():
    request_data = request.get_json()
    idToDelete = request_data['id']
    for i in range(len(investor_tb) -1, -1, -1):
        if investor_tb[i]["ID"] == idToDelete:
            #query to delete where the id matches
            query = "DELETE FROM investor WHERE ID = %s" %(idToDelete)
            execute_query(conn, query)
            return "delete request successful"

#add stock
@app.route('/api/addstock', methods=['POST'])
def api_add():
    request_data = request.get_json()
    new_stockname = request_data['stockname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = '''INSERT INTO stock (stockname, abbreviation, currentprice)
    VALUES ('%s','%s', %s )''' %(new_stockname, new_abbr, new_price)
    execute_query(conn,query)
    return "add reqeust successful"

#edit stock
@app.route('/api/edit_stock', methods=['PUT'])
def api_update_all():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newsname = request_data["stockname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    for i in range(len(stock_tb)):
        if stock_tb[i]['ID'] == idToUpdate:
            query = """UPDATE stock 
            SET stockname = '%s', abbreviation = '%s', currentprice = %s
            WHERE id = %s""" %(newsname, newabb, newprice, idToUpdate)
            execute_query(conn, query)
            return "stock edit was successful"

#delete stock
@app.route('/api/delete_stock', methods=['DELETE'])
def api_delete():
    request_data = request.get_json()
    idToDelete = request_data['id']
    for i in range(len(stock_tb) -1, -1, -1):
        if stock_tb[i]["ID"] == idToDelete:
            #query to delete where the id matches
            query = "DELETE FROM stock WHERE ID = %s" %(idToDelete)
            execute_query(conn, query)
            return "delete request successful"

#add bond
@app.route('/api/add_bond', methods=['POST'])
def api_add():
    request_data = request.get_json()
    new_stockname = request_data['bondname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = '''INSERT INTO bond (stockname, abbreviation, currentprice)
    VALUES ('%s','%s', %s )''' %(new_stockname, new_abbr, new_price)
    execute_query(conn,query)
    return "add reqeust successful"

#edit bond
@app.route('/api/edit_bond', methods=['PUT'])
def api_update_all():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newbname = request_data["bondname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    for i in range(len(bond_tb)):
        if bond_tb[i]['ID'] == idToUpdate:
            query = """UPDATE stock 
            SET stockname = '%s', abbreviation = '%s', currentprice = %s
            WHERE id = %s""" %(newbname, newabb, newprice, idToUpdate)
            execute_query(conn, query)
            return "bond edit was successful"

#delete bond
@app.route('/api/delete_bond', methods=['DELETE'])
def api_delete():
    request_data = request.get_json()
    idToDelete = request_data['id']
    for i in range(len(bond_tb) -1, -1, -1):
        if bond_tb[i]["ID"] == idToDelete:
            #query to delete where the id matches
            query = "DELETE FROM bond WHERE ID = %s" %(idToDelete)
            execute_query(conn, query)
            return "delete request successful"
        
# Eman's Part
# Investor Portfolio (Stocks and Bonds)
@app.route('/api/investor_portfolio', methods=['GET'])
def api_investor_portfolio():
    request_data = request.get_json()
    investor_id = request_data['investorid']

    stock_query = f"SELECT s.stockname, st.quantity FROM stocktransaction st JOIN stock s ON st.stockid = s.id WHERE st.investorid = {investor_id}"
    stock_portfolio = execute_read_query(conn, stock_query)

    bond_query = f"SELECT b.bondname, bt.quantity FROM bondtransaction bt JOIN bond b ON bt.bondid = b.id WHERE bt.investorid = {investor_id}"
    bond_portfolio = execute_read_query(conn, bond_query)

    return jsonify({
        'stocks': stock_portfolio,
        'bonds': bond_portfolio
    })

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