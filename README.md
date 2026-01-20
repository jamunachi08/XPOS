# AlphaX POS Suite (Frappe / ERPNext v15+)

**AlphaX POS Suite** is a unified, ERPNext-integrated POS foundation designed to work across:
- Restaurant / Café (tables, KDS, kitchen stations)
- Retail (quick sale, barcode)
- Pharmacy (batch/expiry-ready via ERPNext stock features)
- Any POS environment that posts to **ERPNext Sales Invoice** and supports **multi-payment**, **roles**, and **audit trails**.

This repository is a **ready-to-install Frappe app** (Frappe v15+).  
It provides a production-safe **baseline** and an extensible architecture.

## Key Concepts
- **POS Order**: a lightweight transactional doctype that can post to ERPNext **Sales Invoice**.
- **Posting Service**: centralized, testable Python service that creates/updates Sales Invoice and related records.
- **KDS Ticket**: optional kitchen screen workflow for F&B.
- **Outlet / Terminal**: configuration layer for multi-branch / multi-warehouse operations.
- **Roles & Permissions**: cashier/supervisor/manager/kitchen and system roles.

## Install (Bench)
```bash
bench get-app https://github.com/<your-org>/alphax_pos_suite
bench --site <site-name> install-app alphax_pos_suite
bench --site <site-name> migrate
```

## Quick Setup
1. Go to **AlphaX POS Suite > Setup**
2. Create **POS Outlet** (company, branch, default warehouse)
3. Create **POS Terminal** (outlet, default mode of payment, naming series)
4. Create **POS Order** and submit → posts ERPNext **Sales Invoice** (if enabled)

## Compatibility
- Frappe v15+
- ERPNext v15+
- Works with standard ERPNext items, price lists, taxes, warehouses, stock, customers.

## License
MIT (see license.txt)
