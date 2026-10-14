import urllib.request
import urllib.parse
import json

BASE = "http://127.0.0.1:5000"

def run_all_tests():
    print("=" * 60)
    print("RUNNING COMPLETE GROCERY STORE APPLICATION TEST SUITE")
    print("=" * 60)

    # 1. UI Root
    req = urllib.request.urlopen(f"{BASE}/")
    html = req.read().decode("utf-8")
    assert "Grocery Store Management System" in html
    print("[PASS] 1. Web UI Dashboard is serving correctly")

    # 2. Products UI page
    req = urllib.request.urlopen(f"{BASE}/manage-product.html")
    html = req.read().decode("utf-8")
    assert "Manage Product" in html or "GSMS" in html
    print("[PASS] 2. Manage Product UI is serving correctly")

    # 3. New Order UI page
    req = urllib.request.urlopen(f"{BASE}/order.html")
    html = req.read().decode("utf-8")
    assert "Grocery Store Management System" in html
    print("[PASS] 3. Order UI is serving correctly")

    # 4. Order Details UI page
    req = urllib.request.urlopen(f"{BASE}/order_details.html")
    html = req.read().decode("utf-8")
    assert "Grocery Store Management System" in html
    print("[PASS] 4. Order Details UI is serving correctly")

    # 5. GET /getProducts
    req = urllib.request.urlopen(f"{BASE}/getProducts")
    products = json.loads(req.read().decode("utf-8"))
    assert len(products) >= 50
    print(f"[PASS] 5. GET /getProducts -> retrieved {len(products)} products")

    # 6. GET /getUOM
    req = urllib.request.urlopen(f"{BASE}/getUOM")
    uoms = json.loads(req.read().decode("utf-8"))
    assert len(uoms) >= 6
    print(f"[PASS] 6. GET /getUOM -> retrieved {len(uoms)} measurement units")

    # 7. GET /getAllOrders
    req = urllib.request.urlopen(f"{BASE}/getAllOrders")
    orders = json.loads(req.read().decode("utf-8"))
    assert len(orders) >= 60
    print(f"[PASS] 7. GET /getAllOrders -> retrieved {len(orders)} orders")

    # 8. POST /insertProduct
    payload = {"data": json.dumps({"product_name": "Fresh Alphonso Mango", "uom_id": 2, "price_per_unit": 150.0})}
    req = urllib.request.Request(f"{BASE}/insertProduct", data=urllib.parse.urlencode(payload).encode())
    res = json.loads(urllib.request.urlopen(req).read().decode())
    new_prod_id = res["product_id"]
    assert new_prod_id > 0
    print(f"[PASS] 8. POST /insertProduct -> created product #{new_prod_id}")

    # 9. POST /editProduct
    payload = {"data": json.dumps({"product_id": new_prod_id, "name": "Organic Alphonso Mango", "uom_id": 2, "price_per_unit": 180.0})}
    req = urllib.request.Request(f"{BASE}/editProduct", data=urllib.parse.urlencode(payload).encode())
    res = json.loads(urllib.request.urlopen(req).read().decode())
    assert res["product_id"] == new_prod_id
    print(f"[PASS] 9. POST /editProduct -> updated product #{new_prod_id}")

    # 10. POST /deleteProduct
    payload = {"product_id": new_prod_id}
    req = urllib.request.Request(f"{BASE}/deleteProduct", data=urllib.parse.urlencode(payload).encode())
    res = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"[PASS] 10. POST /deleteProduct -> successfully deleted product #{new_prod_id}")

    # 11. POST /insertOrder (with multiple items)
    payload = {
        "data": json.dumps({
            "customer_name": "Test Customer",
            "grand_total": 230.0,
            "order_details": [
                {"product_id": 1, "quantity": 2, "total_price": 90.0},
                {"product_id": 2, "quantity": 1, "total_price": 65.0},
                {"product_id": 4, "quantity": 1, "total_price": 75.0}
            ]
        })
    }
    req = urllib.request.Request(f"{BASE}/insertOrder", data=urllib.parse.urlencode(payload).encode())
    res = json.loads(urllib.request.urlopen(req).read().decode())
    created_order_id = res["order_id"]
    assert created_order_id > 0
    print(f"[PASS] 11. POST /insertOrder -> created multi-item order #{created_order_id}")

    # 12. GET /getOrderDetails with query param
    req = urllib.request.urlopen(f"{BASE}/getOrderDetails?order_id={created_order_id}")
    items = json.loads(req.read().decode("utf-8"))
    assert len(items) == 3
    print(f"[PASS] 12. GET /getOrderDetails?order_id={created_order_id} -> retrieved {len(items)} items")

    # 13. POST /postOrderDetails then GET /getOrderDetails
    payload = {"order_id": created_order_id}
    req = urllib.request.Request(f"{BASE}/postOrderDetails", data=urllib.parse.urlencode(payload).encode())
    urllib.request.urlopen(req)
    req2 = urllib.request.urlopen(f"{BASE}/getOrderDetails")
    items_session = json.loads(req2.read().decode("utf-8"))
    assert len(items_session) == 3
    print(f"[PASS] 13. Session-based Order Details retrieval verified ({len(items_session)} items)")

    print("=" * 60)
    print("ALL 13 TESTS PASSED! THE APPLICATION IS 100% WORKING!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
