frappe.pages['alphax-pos-setup'].on_page_load = function(wrapper) {
    frappe.ui.make_app_page({
        parent: wrapper,
        title: 'AlphaX POS Suite — Setup',
        single_column: true
    });

    const html = `
      <div class="p-4">
        <div class="alert alert-info">
          <b>AlphaX POS Suite</b> is installed. Use the steps below to configure outlets and terminals.
        </div>

        <h4 class="mt-3">1) Create Outlet</h4>
        <p>Create a <b>AlphaX POS Outlet</b> with company, branch, and default warehouse.</p>
        <p><a class="btn btn-default btn-sm" href="#List/AlphaX POS Outlet/List">Open Outlets</a></p>

        <h4 class="mt-3">2) Create Terminal</h4>
        <p>Create a <b>AlphaX POS Terminal</b> and link it to the outlet.</p>
        <p><a class="btn btn-default btn-sm" href="#List/AlphaX POS Terminal/List">Open Terminals</a></p>

        <h4 class="mt-3">3) Review Settings</h4>
        <p>Enable/disable auto posting, KDS, approvals, and other controls.</p>
        <p><a class="btn btn-default btn-sm" href="#Form/AlphaX POS Settings/AlphaX POS Settings">Open Settings</a></p>

        <h4 class="mt-3">4) Create an Order</h4>
        <p>Create a <b>AlphaX POS Order</b>, add items and payments, and submit. It posts ERPNext <b>Sales Invoice</b>.</p>
        <p><a class="btn btn-primary btn-sm" href="#List/AlphaX POS Order/List">Open POS Orders</a></p>

        <hr/>
        <small class="text-muted">AlphaX POS Suite • Foundation build (v0.1.0)</small>
      </div>
    `;
    $(wrapper).html(html);
};
