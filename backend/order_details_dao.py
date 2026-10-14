from datetime import datetime
from sql_connection import get_sql_connection


__postOrderId = None

def post_order_details(connection, order_id):
    global __postOrderId 
    __postOrderId = order_id
    return __postOrderId

def get_order_details(connection, order_id=None):
    global __postOrderId
    target_id = order_id if order_id is not None else __postOrderId
    if target_id is None:
        return []

    cursor = connection.cursor()
    query = (
        "SELECT order_details.order_id, product.name, product.price_per_unit, "
        "uom.uom_name, order_details.quantity, order_details.total_price "
        "FROM gs.order_details "
        "INNER JOIN gs.product ON order_details.product_id = product.product_id "
        "INNER JOIN gs.uom ON product.uom_id = uom.uom_id "
        "WHERE order_details.order_id = %s"
    )
    cursor.execute(query, (target_id,))

    response = []
    for order_id_val, name, price_per_unit, uom_name, quantity, total_price in cursor:
        response.append(
            {
                "order_id": order_id_val,
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
    
