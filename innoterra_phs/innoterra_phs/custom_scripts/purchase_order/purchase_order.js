frappe.ui.form.on('Purchase Order', {

    refresh: function(frm){
       frm.add_custom_button(('Create Sales Order'), function(){
        frappe.model.open_mapped_doc({
            method: "innoterra_phs.innoterra_phs.custom_scripts.purchase_order.purchase_order.make_Sales_order",
            frm: cur_frm
       }, ('Create')); 
    })
  }
});
