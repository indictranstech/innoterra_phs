frappe.ui.form.on('Address', {
	refresh(frm) {
	  if(frappe.user.has_role("PHS")===false){
	      frm.set_df_property("city", "reqd", 1);
	  }
	},
	village(frm) {
	    if(frappe.user.has_role("PHS"))   {
	        frm.set_value("city", frm.doc.village);
	    }
	}
})
