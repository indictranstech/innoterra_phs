// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Harvest Intimation', {
	refresh: function(frm) {
		if(frm.doc.docstatus!=2)	{
			frm.add_custom_button(("Create Collection Intimation"), function() {
				frappe.model.open_mapped_doc({
					method: "innoterra_phs.innoterra_phs.doctype.harvest_intimation.harvest_intimation.make_collection_intimation",
					frm : cur_frm
				})
			});
		}
	}
});
