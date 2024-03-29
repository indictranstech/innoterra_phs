frappe.ui.form.on('Item Price', {
	refresh(frm) {
	if(!frm.doc.valid_from)	{
		frm.set_value("valid_from", get_today());
		frm.refresh_field("valid_from");
	}
        frm.add_custom_button('Update Open PO', () => {
            frm.events.update_po(frm)
        })

        if(frm.doc.valid_upto){
            frm.set_df_property("valid_upto", "read_only", 1)
            frm.refresh_field("valid_upto")
        }

	},
    update_po : function(frm) {
        // let ed= frm.doc.valid_upto
        // if(frm.doc.valid_upto ==undefined || frm.doc.valid_upto == ""){
        //     ed= frappe.datetime.get_today()

        // }
        console.log(" this is dates ", frm.doc.valid_from , frm.doc.valid_upto)
        if(frm.doc.valid_from && !frm.doc.valid_upto){
        frappe.call({
                "method":"innoterra_phs.innoterra_phs.custom_scripts.item_price.item_price.upate_po",
                "args":{
                     "item_code":frm.doc.item_code,
                     'name' : frm.doc.name,
                     "sd":frm.doc.valid_from,
                     "ed":frm.doc.valid_upto || ""
                    },
                callback:function(r){
                    if(r.message > 0) {
                        frappe.msgprint(__(" {0} Purchase Order is Updated", [r.message]));
                    }
                }

            })
        }    
    },
})
