frappe.ui.form.on('Sales Invoice', {
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
