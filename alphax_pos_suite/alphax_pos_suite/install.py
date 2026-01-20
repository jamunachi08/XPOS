import json
import os

import frappe


def after_install():
    """Create required setup objects for AlphaX POS Suite."""
    create_roles()
    create_custom_fields()


def create_roles():
    """Create POS roles used for UI permission gating."""
    roles = [
        "AlphaX POS Cashier",
        "AlphaX POS Supervisor",
        "AlphaX POS Manager",
    ]

    for role in roles:
        if not frappe.db.exists("Role", role):
            doc = frappe.get_doc({"doctype": "Role", "role_name": role})
            doc.insert(ignore_permissions=True)


def _seed_custom_fields():
    seed_path = os.path.join(os.path.dirname(__file__), "data", "custom_fields_seed.json")
    if not os.path.exists(seed_path):
        return []
    with open(seed_path, encoding="utf-8") as f:
        return json.load(f)


def create_custom_fields():
    """Create Custom Fields required by the suite."""
    try:
        from frappe.custom.doctype.custom_field.custom_field import create_custom_field
    except Exception:
        return

    for row in _seed_custom_fields():
        if row.get("doctype") != "Custom Field":
            continue

        dt = row.get("dt")
        fieldname = row.get("fieldname")
        if not dt or not fieldname:
            continue

        if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
            continue

        df = dict(row)
        df.pop("doctype", None)
        df.pop("dt", None)

        # create_custom_field signature differs slightly across versions
        try:
            create_custom_field(dt, df, ignore_validate=True)
        except TypeError:
            create_custom_field(dt, df)
