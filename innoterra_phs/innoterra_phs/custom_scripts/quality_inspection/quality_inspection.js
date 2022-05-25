
frappe.ui.form.on("Quality Inspection", {
    refresh:function(frm) {
        frm.add_custom_button("Create Deductible Ratio", 
            () => frm.events.make_dr(frm)
        );

     },

     make_dr : function(frm) {
        frappe.call({
                "method":"innoterra_phs.innoterra_phs.custom_scripts.quality_inspection.quality_inspection.make_deductible_ratio",
                "args":{ doc : frm.doc.name },
                freeze: true,
                callback:function(r){
                    // if(!r.exc) {
                        if(r.message) {
                            frappe.set_route("Form", "Deductible Ratio", r.message);
                    }
               // }
                }

            })

     }

    
});










frappe.set_route("Form", "Deductible Ratio")