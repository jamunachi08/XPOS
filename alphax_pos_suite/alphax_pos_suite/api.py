import frappe

@frappe.whitelist()
def ping():
    return {"ok": True, "app": "alphax_pos_suite"}

@frappe.whitelist()
def redeem_credit_note(credit_note, invoice, amount=None):
    # Accounting-specific: implement Payment Entry / Journal Entry allocations based on your COA.
    return {
        "ok": False,
        "message": "Credit note redemption needs accounting mapping (Payment Entry/Journal Entry). Implement in next iteration based on your Chart of Accounts."
    }

import frappe
from frappe import _

@frappe.whitelist()
def get_pos_boot(terminal):
    if not terminal or not frappe.db.exists("AlphaX POS Terminal", terminal):
        frappe.throw(_("Terminal not found."))

    t = frappe.get_doc("AlphaX POS Terminal", terminal)
    prof_name = getattr(t, "pos_profile", None)
    payload = {"profile": None, "theme": None, "payment_methods": [], "scale": {"generic": None, "prefix_map": []}}

    if prof_name and frappe.db.exists("AlphaX POS Profile", prof_name):
        p = frappe.get_doc("AlphaX POS Profile", prof_name)
        payload["profile"] = {"name": p.name, "pos_type": p.pos_type, "enable_shortcuts": int(p.enable_shortcuts or 0),
                              "enable_scale": int(p.enable_weighing_scale or 0)}
        if p.theme and frappe.db.exists("AlphaX POS Theme", p.theme):
            th = frappe.get_doc("AlphaX POS Theme", p.theme)
            payload["theme"] = {
                "primary": th.primary_color, "secondary": th.secondary_color, "accent": th.accent_color,
                "danger": th.danger_color, "bg": th.bg_color, "card": th.card_bg, "text": th.text_color,
                "radius": int(th.button_radius or 12), "touch": int(th.touch_mode or 0), "font": th.font_family
            }

        if int(p.use_profile_payment_methods or 0) == 1:
            rows = sorted(p.payment_methods or [], key=lambda r: int(getattr(r, "sort_order", 0) or 0))
            payload["payment_methods"] = [{"mode_of_payment": r.mode_of_payment, "is_default": int(r.is_default or 0), "color": r.button_color} for r in rows]

        if int(p.enable_weighing_scale or 0) == 1:
            if p.generic_scale_definition and frappe.db.exists("AlphaX POS Scale Barcode Definition", p.generic_scale_definition):
                d = frappe.get_doc("AlphaX POS Scale Barcode Definition", p.generic_scale_definition)
                payload["scale"]["generic"] = _def_to_dict(d)

            rules = sorted(p.scale_rules or [], key=lambda r: int(getattr(r, "priority", 10) or 10))
            for r in rules:
                if r.applies_to == "Barcode Prefix" and r.barcode_prefix and r.definition and frappe.db.exists("AlphaX POS Scale Barcode Definition", r.definition):
                    d = frappe.get_doc("AlphaX POS Scale Barcode Definition", r.definition)
                    payload["scale"]["prefix_map"].append({"prefix": r.barcode_prefix, "defn": _def_to_dict(d)})

    return payload

def _def_to_dict(d):
    return {
        "prefix": d.prefix or "",
        "total_length": int(d.total_length or 0),
        "mapping_type": d.mapping_type,
        "qty_divider": float(d.qty_divider or 1),
        "rate_divider": float(d.rate_divider or 1),
        "use_qty_from_barcode": int(d.use_qty_from_barcode or 0),
        "use_rate_from_barcode": int(d.use_rate_from_barcode or 0),
        "item_start": int(d.item_start or 1), "item_length": int(d.item_length or 4),
        "qty_start": int(d.qty_start or 5), "qty_length": int(d.qty_length or 4),
        "rate_start": int(d.rate_start or 9), "rate_length": int(d.rate_length or 4),
    }

@frappe.whitelist()
def get_kb_articles(role=None):
    roles = set(frappe.get_roles(frappe.session.user))
    kb_roles = []
    if "System Manager" in roles or "POS Manager" in roles:
        kb_roles = ["Cashier","Supervisor","Manager","Implementer"]
    elif "POS Supervisor" in roles:
        kb_roles = ["Cashier","Supervisor"]
    else:
        kb_roles = ["Cashier"]
    if role and role in kb_roles:
        kb_roles = [role]
    return frappe.get_all("AlphaX POS KB Article",
        filters={"enabled":1, "role":["in", kb_roles]},
        fields=["name","title","role","section","shortcut","content"],
        order_by="role asc, section asc, title asc"
    )

@frappe.whitelist()
def terminal_capture_start(mode_of_payment, amount, currency=None, terminal=None):
    return {
        "status": "PENDING",
        "mode_of_payment": mode_of_payment,
        "amount": amount,
        "currency": currency,
        "message": "Terminal integration is enabled but driver is not configured yet."
    }
