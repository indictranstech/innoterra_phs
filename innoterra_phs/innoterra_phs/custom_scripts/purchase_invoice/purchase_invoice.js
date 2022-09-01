frappe.ui.form.on('Purchase Invoice', {
    
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