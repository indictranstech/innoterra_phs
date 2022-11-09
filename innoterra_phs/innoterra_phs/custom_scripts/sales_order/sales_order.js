frappe.ui.form.on('Sales Order', {
    
    setup: function (frm) {
       if( frm.doc.is_internal_customer == 0 && (frm.doc.po_number !== undefined || frm.doc.po_number !== "" ) ){
           
       frm.set_value('inter_company_order_reference',"")
       frm.set_value('po_number',"")
       frm.set_value('customer',"")
       frm.set_value('represents_company',"")
       frm.set_value('is_internal_customer',0)
 
        frm.refresh_field('inter_company_order_reference');
       frm.refresh_field('po_number');
       frm.refresh_field('customer');
       frm.refresh_field('represents_company');
       frm.refresh_field('is_internal_customer');
 
 
       $.each(frm.doc.items || [], function (i, v) {
           console.log(v)
         frappe.model.set_value(v.doctype, v.name, "delivery_by_supplier",0)
         frappe.model.set_value(v.doctype, v.name, "prevdoc_docname","")
 
       })
       frm.refresh_field('items');
 
    }
    },
    is_vla(frm) {
        frm.set_query('vla', () => {
            return {
                filters: {
                    is_vla: frm.doc.is_vla
                }
            }
        });
    }
 
 })
