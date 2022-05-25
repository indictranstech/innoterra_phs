// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deductible Ratio', {
	 on_submit: function(frm) {
		frm.add_custom_button("Create Item Price", 
			() => frm.events.add_price(frm)
        );

	 },
	 add_price : function(frm) {
	 	var price_rate;
	 	var price_list;
	 	$.each(frm.doc.revised_price_table, function(idx, row){
							if (row.status == "Accepted") {
								price_rate = row.revised_price;
								price_list = row.price_list;
							}
							});
	 	frappe.call({
                "method":"innoterra_phs.innoterra_phs.doctype.deductible_ratio.deductible_ratio.add_pricelist",
                "args": { item : frm.doc.item_code,
                	    rate : price_rate,
                		price_list : price_list},
                callback:function(r){
					if(r.message) {
   							frappe.msgprint("New price is created ");
                         }
						}
			})

                }

	 });


