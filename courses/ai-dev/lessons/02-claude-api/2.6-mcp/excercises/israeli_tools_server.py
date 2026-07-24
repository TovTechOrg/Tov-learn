from fastmcp import FastMCP

mcp = FastMCP(name="שרת כלים ישראליים")


@mcp.tool()
def validate_israeli_business_id(business_id: str) -> dict:
    """
    Validates an Israeli business ID (H.P. or O.M.).
    It checks if the ID has 9 digits and if the check digit is correct.
    :param business_id: The 9-digit Israeli business ID string.
    :return: A dictionary with 'valid' (boolean) and a 'message'.
    """
    if not business_id.isdigit() or len(business_id) != 9:
        return {"valid": False, "message": "Business ID must be exactly 9 digits."}

    total = 0
    for i, ch in enumerate(business_id):
        digit = int(ch)
        weight = 1 if i % 2 == 0 else 2
        product = digit * weight
        if product >= 10:
            product -= 9  # digit sum of a two-digit number formed by digit*weight (max 18)
        total += product

    if total % 10 == 0:
        return {"valid": True, "message": "Business ID is valid."}
    return {"valid": False, "message": "Business ID is invalid (checksum failed)."}


@mcp.tool()
def get_interest_rate_boi() -> dict:
    """
    Gets the current official interest rate from the Bank of Israel.
    :return: A dictionary with the rate and the last update date.
    """
    # In a real scenario, this would make an API call.
    # For this exercise, we return a mocked, hard-coded value.
    return {
        "rate_percent": 4.5,
        "last_update": "2026-05-10",
        "source": "Bank of Israel (Mock Data)",
    }




REGULATIONS_INFO = """
# תקציר רגולציה לפתיחת עסק בישראל

1.  **רישום ברשויות:** יש להירשם כעוסק מורשה/פטור, ולקבל מספר עוסק ממע"מ.
2.  **צורת התאגדות:** נדרש להחליט אם עוסק פטור, עוסק מורשה או חברה בע"מ.
3.  **רישיון עסק:** עסקים מסוימים (כמו מסעדות) דורשים רישיון עסק מהרשות המקומית.
"""


@mcp.resource("resource://israeli-business-regulations")
def israeli_business_regulations() -> str:
    """Provides a summary of regulations for opening a new business in Israel."""
    return REGULATIONS_INFO


if __name__ == "__main__":
    mcp.run()