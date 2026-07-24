BASE = 10
RATE = 2.5

peak_hours = {8, 9, 10, 17, 18, 19, 20}

orders = []


def calc(d, t):
    if d < 0:
        raise ValueError(f"Distance must be non-negative, got {d}")
    if not 0 <= t <= 23:
        raise ValueError(f"Hour must be 0-23, got {t}")

    if t in peak_hours:
        total = BASE + (d * RATE * 1.5)
    else:
        total = BASE + (d * RATE)

    orders.append(total)
    return total


def get_orders():
    return list(orders)


def most_expensive():
    if not orders:
        return None
    return max(orders)
