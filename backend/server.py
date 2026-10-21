import os
import json
from flask import Flask, request, jsonify, send_from_directory
from sql_connection import get_sql_connection
import product_dao
import orders_dao
import uom_dao
import order_details_dao

# Path to the ui directory
UI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui")

app = Flask(__name__, static_folder=UI_DIR, static_url_path="")


def get_db_connection():
    return get_sql_connection()


# ----------------------------------------------------
# Frontend Routes (Serve UI directly on port 5000)
# ----------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(UI_DIR, "index.html")


@app.route("/<path:path>")
def serve_ui(path):
    file_path = os.path.join(UI_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(UI_DIR, path)
    return send_from_directory(UI_DIR, "index.html")


# ----------------------------------------------------
# API Endpoints
# ----------------------------------------------------
@app.route("/getProducts", methods=["GET"])
def get_Products():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    products = product_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/postOrderDetails', methods=['POST'])
def post_order_details():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    order_id = order_details_dao.post_order_details(connection, request.form["order_id"])
    response = jsonify(order_id)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response    
    

@app.route("/getOrderDetails", methods=["GET"])
def get_order_details():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    order_id = request.args.get("order_id")
    order_details = order_details_dao.get_order_details(connection, order_id)
    response = jsonify(order_details)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/editProduct', methods=['POST', 'GET'])
def edit_product():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    request_payload = json.loads(request.form['data'])
    product_id = product_dao.edit_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    return_id = product_dao.delete_product(connection, request.form["product_id"])
    response = jsonify({"product_id": return_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getUOM", methods=["GET"])
def get_uom():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    request_payload = json.loads(request.form["data"])
    product_id = product_dao.insert_new_product(connection, request_payload)
    response = jsonify({"product_id": product_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/insertOrder", methods=["POST"])
def insert_order():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    request_payload = json.loads(request.form["data"])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({"order_id": order_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getAllOrders", methods=['GET'])
def get_all_orders():
    connection = get_db_connection()
    if connection is None:
        res = jsonify({"error": "Database connection unavailable. Ensure MySQL/XAMPP is running."})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 503

    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    print("Starting Python Flask server for Grocery Store Management System")
    # Pre-check database connection
    get_sql_connection()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

