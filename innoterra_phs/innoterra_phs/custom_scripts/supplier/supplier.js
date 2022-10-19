frappe.ui.form.on("Supplier", {
	before_save: function (frm) {
        
		if (frm.doc.is_farmer == 1) {
			frm.set_value("supplier_type", 'Individual');
            refresh_field("supplier_type")
            cur_frm.save();
		}
      }
    })
