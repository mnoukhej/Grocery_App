from sql_connection import get_sql_connection


def get_all_products(connection):
    cursor = connection.cursor()

    query = (
        "SELECT product.product_id, product.name, product.uom_id, product.price_per_unit, uom.uom_name "
        "FROM gs.product inner join gs.uom on product.uom_id=uom.uom_id;"
    )

    # query = (
    #     "SELECT CONCAT('PROD', LPAD(product.product_id, 4, '0')) AS formatted_product_id, "
    #     "product.name,product.uom_id, product.price_per_unit, uom.uom_name "
    #     "FROM gs.product INNER JOIN gs.uom ON product.uom_id = uom.uom_id ORDER BY product.name;"
    # )

    cursor.execute(query)

    response = []

    for product_id, name, uom_id, price_per_unit, uom_name in cursor:
        response.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_name,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name,
            }
        )
    return response


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = (
        "INSERT INTO gs.product (name, uom_id, price_per_unit) VALUES (%s,%s,%s);"
    )
    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def edit_product(connection, product):
    cursor = connection.cursor()
    query = ("UPDATE product "
             "set name=%s, uom_id=%s, price_per_unit=%s"
             " WHERE product_id=%s;")
    data = (product['name'], product['uom_id'], product['price_per_unit'], product['product_id'])

    cursor.execute(query, data)
    connection.commit()

    return product['product_id']


def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM gs.product WHERE product_id= " + str(product_id)
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid


if __name__ == "__main__":
    connection = get_sql_connection()
    # print(get_all_products(connection))

    print(
        insert_new_product(
            connection,
            {"product_name": "cabbage", "uom_id": "1", "price_per_unit": "10"},
        )
    )

    # print(delete_product(connection, 20))
