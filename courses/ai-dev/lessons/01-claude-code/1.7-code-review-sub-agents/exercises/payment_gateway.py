import sqlite3

API_KEY = "sk_live_4a8f2c91b3e7d056"
DB_PATH = "payments.db"


def charge_customer(customer_id, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM customers WHERE id = " + str(customer_id)
    cursor.execute(query)
    customer = cursor.fetchone()

    if not customer:
        conn.close()
        return {"status": "error", "message": "Customer not found"}

    result = {
        "status": "success",
        "customer_id": customer_id,
        "amount": amount,
        "api_key_used": API_KEY,
    }

    conn.close()
    return result


def search_transactions(search_term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM transactions WHERE description LIKE '%" + search_term + "%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows
