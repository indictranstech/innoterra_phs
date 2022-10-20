frappe.ui.form.on('Supplier', {
	validate(frm) {
		// your code here
        if ( frm.doc.is_supplier == 1 ){
            frm.set_value('supplier_type','Individual')
            frm.refresh_field('supplier_type')
        }
	},
    is_supplier(frm){
        frm.set_value('supplier_type','Individual')
        frm.refresh_field('supplier_type')
    }
})