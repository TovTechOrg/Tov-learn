import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.monday_fake_token_123"
BOARD_ID = 9876543210

BASE_URL = "https://api.monday.com/v2"

def run_query(q):
    r = requests.post(
        BASE_URL,
        headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
        json={"query": q},
    )
    return r.json()

def get_items(board_id, filter_val):
    query = """
    {
      boards(ids: """ + str(board_id) + """) {
        items_page {
          items {
            id name
            column_values { id text }
          }
        }
      }
    }
    """
    data = run_query(query)
    items = data["data"]["boards"][0]["items_page"]["items"]

    result = []
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i]["id"] == items[j]["id"]:
                if items[i] not in result:
                    result.append(items[i])
    return result

def create_item(board_id, item_name, col_vals):
    mutation = 'mutation { create_item (board_id: ' + str(board_id) + ', item_name: "' + item_name + '") { id } }'
    return run_query(mutation)

def update_status(item_id, status):
    mutation = """
    mutation {
      change_simple_column_value(
        item_id: """ + str(item_id) + """,
        board_id: """ + str(BOARD_ID) + """,
        column_id: "status",
        value: \"""" + status + """\"
      ) { id }
    }
    """
    return run_query(mutation)
