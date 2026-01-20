import frappe

CHILD_TABLES = [
    "AlphaX POS Profile Payment Method",
    "AlphaX POS Scale Barcode Rule",
    "AlphaX POS Email Recipient",
]


def _ensure_parent_columns(table_name: str) -> None:
    if not frappe.db.table_exists(table_name):
        return

    safe = table_name.replace("`", "")
    cols = {c[0] for c in frappe.db.sql("SHOW COLUMNS FROM `{}`".format(safe))}

    if "parent" not in cols:
        frappe.db.sql("ALTER TABLE `{}` ADD COLUMN parent varchar(140)".format(safe))
    if "parenttype" not in cols:
        frappe.db.sql("ALTER TABLE `{}` ADD COLUMN parenttype varchar(140)".format(safe))
    if "parentfield" not in cols:
        frappe.db.sql("ALTER TABLE `{}` ADD COLUMN parentfield varchar(140)".format(safe))
    if "idx" not in cols:
        frappe.db.sql("ALTER TABLE `{}` ADD COLUMN idx int(8) DEFAULT 0".format(safe))

    # helpful index for loading child rows
    try:
        frappe.db.sql("ALTER TABLE `{}` ADD INDEX idx_parent (parent)".format(safe))
    except Exception:
        pass


def execute():
    for dt in CHILD_TABLES:
        _ensure_parent_columns("tab{}".format(dt))
