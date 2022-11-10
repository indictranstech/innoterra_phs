frappe.ui.form.on('Item Price', {
	refresh(frm) {
	if(!frm.doc.valid_from)	{
		frm.set_value("valid_from", get_today());
		frm.refresh_field("valid_from");
	}
        frm.add_custom_button('Update Open PO', () => {
            frm.events.update_po(frm)
        })


	},
    update_po : function(frm) {
        let ed= frm.doc.valid_upto
        if(frm.doc.valid_upto ==undefined || frm.doc.valid_upto == ""){
            ed= frappe.datetime.get_today()

        }
        frappe.call({
                "method":"innoterra_phs.innoterra_phs.custom_scripts.item_price.item_price.upate_po",
                "args":{
                     "item_code":frm.doc.item_code,
                     'name' : frm.doc.name,
                     "sd":frm.doc.valid_from,
                     "ed":ed
                    },
                callback:function(r){
                    // if(!r.exc) {
                        if(r.message) {
                            frappe.msgprint("Purchase Order is Updated");
                    }
               // }
                }

            })

     }



})
