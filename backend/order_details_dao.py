from datetime import datetime
from sql_connection import get_sql_connection


__postOrderId = None

def post_order_details(connection, order_id):
    global __postOrderId 
    __postOrderId = order_id
    return __postOrderId

def get_order_details(connection):
    cursor = connection.cursor()

    query = ("SELECT * FROM (SELECT order_details.order_id, product.name, product.price_per_unit,"
            "uom.uom_name, order_details.quantity, order_details.total_price "
            "FROM gs.order_details "
            "INNER JOIN gs.product ON order_details.product_id = product.product_id "
            "INNER JOIN gs.uom ON product.uom_id = uom.uom_id) AS subquery_alias "
            "WHERE order_id = "+ str(__postOrderId))  
    
    # cursor.execute(query, (__postOrderId,))  


    # query = (
    #     "SELECT order_details.order_id, product.name, product.price_per_unit, uom.uom_name, "
    #     "order_details.quantity, order_details.total_price "
    #     "FROM gs.order_details "
    #     "INNER JOIN gs.product ON order_details.product_id = product.product_id "
    #     "INNER JOIN gs.uom ON product.uom_id = uom.uom_id"
    # )
    cursor.execute(query)


    response = []
    for order_id, name, price_per_unit, uom_name, quantity, total_price in cursor:
        response.append(
            {
                "order_id": order_id,
                "name": name,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name,
                "quantity": quantity,
                "total_price": total_price
            }
        )
    return response




if __name__ == '__main__':
    connection = get_sql_connection()
    # order_id = 1
    # post_order_details(connection, order_id)
    # get_order_details(connection)
    
