from fastmcp import FastMCP

mcp = FastMCP(name="שרת תמיכה באתרי Wix")

# --- Mock data ---
_SITES = {
    "site_123": {
        "site_name": "החנות של דנה",
        "created_date": "2025-03-14",
        "connected_to_premium_domain": True,
        "installed_apps": ["Wix Stores", "Wix Chat"],
    },
    "site_456": {
        "site_name": "אתר תדמית - סטודיו יוגה",
        "created_date": "2026-01-02",
        "connected_to_premium_domain": False,
        "installed_apps": ["Wix Bookings"],
    },
}

_TAKEN_DOMAINS = {"danas-shop.com", "yoga-studio.co.il"}


@mcp.tool()
def get_site_details(site_id: str) -> dict:
    """
    Gets basic details for a Wix site: name, creation date, and premium domain status.
    :param site_id: The Wix site identifier.
    :return: A dictionary with site details, or an error message if the site is not found.
    """
    site = _SITES.get(site_id)
    if site is None:
        return {"error": f"Site '{site_id}' not found."}
    return {
        "site_id": site_id,
        "site_name": site["site_name"],
        "created_date": site["created_date"],
        "connected_to_premium_domain": site["connected_to_premium_domain"],
    }


@mcp.tool()
def check_domain_status(domain_name: str) -> dict:
    """
    Checks whether a domain is free, already connected to a Wix site, or taken elsewhere.
    :param domain_name: The domain name to check, e.g. "example.com".
    :return: A dictionary with the domain's status.
    """
    if domain_name in _TAKEN_DOMAINS:
        return {"domain": domain_name, "status": "taken", "message": "Domain is already connected to a Wix site."}
    return {"domain": domain_name, "status": "available", "message": "Domain is free to connect."}


@mcp.tool()
def list_installed_apps(site_id: str) -> dict:
    """
    Lists the Wix apps (e.g. Wix Stores, Wix Bookings) installed on a given site.
    :param site_id: The Wix site identifier.
    :return: A dictionary with the list of installed apps, or an error if the site is not found.
    """
    site = _SITES.get(site_id)
    if site is None:
        return {"error": f"Site '{site_id}' not found."}
    return {"site_id": site_id, "installed_apps": site["installed_apps"]}


@mcp.tool()
def add_user_to_role(site_id: str, user_email: str, role: str, confirm: bool = False) -> dict:
    """
    Grants a user a role (e.g. "Editor" or "Owner") on a Wix site.
    This is a sensitive, real-world action — it must NOT run without explicit confirmation.
    Call this once with confirm=False to preview the change, then call it again with
    confirm=True only after the user has explicitly confirmed the email and role.
    :param site_id: The Wix site identifier.
    :param user_email: The email of the user to grant access to.
    :param role: The role to grant, e.g. "Editor", "Owner", "Viewer".
    :param confirm: Must be True to actually perform the change.
    :return: A dictionary describing the pending or completed action.
    """
    if site_id not in _SITES:
        return {"error": f"Site '{site_id}' not found."}

    if not confirm:
        return {
            "status": "pending_confirmation",
            "message": (
                f"About to grant '{role}' access to {user_email} on site '{site_id}'. "
                "Confirm these details with the user, then call this tool again with confirm=True."
            ),
        }

    return {
        "status": "done",
        "message": f"{user_email} was granted '{role}' access on site '{site_id}'.",
    }


if __name__ == "__main__":
    mcp.run()
