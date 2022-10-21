frappe.ui.form.on('Purchase Order', {

    onload(frm){
        // if (){}
        frm.add_custom_button('Sales Order', () => {

            frappe.model.open_mapped_doc({
                method: "innoterra_phs.innoterra_phs.custom_scripts.purchase_order.purchase_order.make_Sales_order",
                frm: cur_frm
            })

        }, 'Create Sales Order', 'primary');
        

    },
    validate(frm){
        if (frappe.datetime.now_date() > cur_frm.doc.transaction_date){
            frappe.validate = false
            frappe.throw(`Date should not be less then  ${frappe.datetime.now_date()}`)
        }

    },
    
    refresh(frm) {
        frm.trigger('get_supplier');
    },
    is_supplier(frm) {
        frm.trigger('get_supplier');
    },
   
    is_transporter(frm) {
        frm.trigger('get_supplier');
    },
    
    is_farmer(frm) {
        frm.trigger('get_supplier');
    },
    
    supplier(frm) {
        frm.trigger('get_supplier');
    },
    is_vla(frm) {
        frm.set_query('vla', () => {
            return {
                filters: {
                    is_vla: frm.doc.is_vla
                }
            }
        });
    },
    set_warehouse(frm) {
        if(frm.doc.set_warehouse != null){
			frappe.call({
				method: "innoterra_phs.innoterra_phs.custom_scripts.purchase_order.purchase_order.get_warehouse_address",
				args:{
					'warehouse': frm.doc.set_warehouse,
				},
				"callback": function(r) {
					if(r.message && r.message.warehouse_address){
                        console.log(r.message);
						frm.set_value("shipping_address",r.message.warehouse_address);
						frm.refresh_field("company_address");
					}
				}
			});
		}
    },
     
    get_supplier(frm) {
        
        let query = {}
        
        if (frm.doc.is_supplier == 1){
            query.is_supplier =1
        }
        
        if (frm.doc.is_transporter == 1){
            query.is_transporter =1
        }        
        
        if (frm.doc.is_farmer == 1){
            query.is_farmer =1
        }
        
        // console.log(query)
    	frm.set_query('supplier', () => {
                return {
                    filters: query
                }
            })
        frm.refresh_field('supplier');

            }
    
    
    
})
