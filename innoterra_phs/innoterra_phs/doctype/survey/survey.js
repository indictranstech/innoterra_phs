// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Survey', {
	refresh: function(frm) {
		if(frm.doc.docstatus!=2)	{
			frm.add_custom_button(("Create Harvest Intimation"), function() {
				frappe.model.open_mapped_doc({
					method: "innoterra_phs.innoterra_phs.doctype.survey.survey.make_harvest_intimation",
					frm : cur_frm
				})
			});
		}
		// To check server update DEC 13 22 10.16
		console.log(" this is for testing Purpose")
	}
	
});




