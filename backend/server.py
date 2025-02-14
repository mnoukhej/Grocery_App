from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import product_dao
import orders_dao
import uom_dao
import order_details_dao
import json

app = Flask(__name__)

connection = get_sql_connection()


@app.route("/")
def index():
    return "Welcome"

@app.route("/getProducts", methods=["GET"])
def get_Products():
    products = product_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/postOrderDetails', methods=['POST'])
def post_order_details():
    order_id = order_details_dao.post_order_details(connection, request.form["order_id"])
    response = jsonify(order_id)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response    
    

@app.route("/getOrderDetails", methods=["GET"])
def get_order_details():
    order_details = order_details_dao.get_order_details(connection)
    #order_details = order_details_dao.get_order_details(connection, request.form['order_id'])
    response = jsonify(order_details)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/editProduct', methods=['POST', 'GET'])
def edit_product():
    request_payload = json.loads(request.form['data'])
    product_id = product_dao.edit_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    return_id = product_dao.delete_product(connection, request.form["product_id"])
    response = jsonify({"product_id": return_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getUOM", methods=["GET"])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    request_pyload = json.loads(request.form["data"])
    product_id = product_dao.insert_new_product(connection, request_pyload)
    response = jsonify({"product_id": product_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/insertOrder", methods=["POST"])
def insert_order():
    request_pyload = json.loads(request.form["data"])
    order_id = orders_dao.insert_order(connection, request_pyload)
    response = jsonify({"order_id": order_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getAllOrders", methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
           




if __name__ == "__main__":
    print("Starting Python Flask server for Grocery Store Management System")
    app.run(port=5000)
