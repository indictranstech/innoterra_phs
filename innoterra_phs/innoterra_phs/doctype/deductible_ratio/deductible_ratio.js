// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deductible Ratio', {
	 on_submit: function(frm) {
		frm.add_custom_button("Create Item Price", 
			() => frm.events.add_price(frm)
        );
	 },
	 refresh:function(frm){
		if (frm.doc.offer_for_price == 1 && frm.doc.docstatus == 1){
			frm.add_custom_button("Create Purchase Order", 
			() => frm.events.Create_price_PO(frm));
		}
		else if(frm.doc.offer_for_quantity == 1 && frm.doc.docstatus == 1){
			frm.add_custom_button("Create Purchase Order", 
			() => frm.events.Create_Qty_PO(frm));
		}
	 },
	 validate:function (frm){
		if (frm.doc.offer_for_price == 1 && frm.doc.offer_for_quantity == 1){
			frappe.validated = false;
			frappe.throw("Offer for price and Offer for Qty could not be check at same time")
		}
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

                },
	 Create_Qty_PO:function(frm){
		frappe.call({
			"method":"innoterra_phs.innoterra_phs.doctype.deductible_ratio.deductible_ratio.Create_Qty_PO",
			"args": { source_name : frm.doc.name},
			callback:function(r){
				if(r.message) {
					// console.log()
						frappe.set_route(['app','purchase-order', r.message])
					 }
					}
		})
	 },
	 Create_price_PO:function(frm){
		frappe.call({
			"method":"innoterra_phs.innoterra_phs.doctype.deductible_ratio.deductible_ratio.Create_price_PO",
			"args": { source_name : frm.doc.name},
			callback:function(r){
				if(r.message) {
					// console.log()
						frappe.set_route(['app','purchase-order', r.message])
					 }
					}
		})
	 },
	})
