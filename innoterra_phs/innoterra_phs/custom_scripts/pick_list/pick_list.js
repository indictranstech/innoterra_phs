frappe.ui.form.on('Pick List', {
	refresh: function(frm) {
        $.each(frm.doc.locations || [], function (i, v) {
            console.log(v);
            frappe.model.set_value(v.doctype, v.name, "warehouse", frm.doc.set_warehouse);
        })
        frm.refresh_field('locations');
	}
});