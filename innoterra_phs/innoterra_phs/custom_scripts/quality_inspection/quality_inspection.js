
frappe.ui.form.on("Quality Inspection", {
    refresh:function(frm) {
            //frm.set_df_property('reference_type', 'hidden', 1);
            frm.set_df_property('reference_type', 'reqd', 0);
            frm.set_df_property('reference_name', 'reqd', 0)
            frm.add_custom_button("Create Deductible Ratio", 
        () => frm.events.make_dr(frm)
        );
    },
     onload :function(frm) {
        frm.set_df_property('reference_type', 'reqd', 0);
            frm.set_df_property('reference_name', 'reqd', 0) 
     },
     on_submit :function(frm) {
        frm.set_df_property('reference_type', 'reqd', 0);
        frm.set_df_property('reference_name', 'reqd', 0);
        frappe.validated = false;

     },
     validate :function(frm) {
        frm.set_df_property('reference_type', 'reqd', 0);
            frm.set_df_property('reference_name', 'reqd', 0);
            //frappe.validated = false; 
     },

    make_dr : function(frm) {
        frappe.call({
                "method":"innoterra_phs.innoterra_phs.custom_scripts.quality_inspection.quality_inspection.make_deductible_ratio",
                "args":{ doc : frm.doc.name },
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

