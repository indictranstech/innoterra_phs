// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
	// refresh: function(frm) {

	// }
	setup: function(frm) {
		//to add now time for in time field
		var today = new Date();
		var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
		var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
		var dateTime = date+' '+time;
		frm.set_value('gate_in_time', dateTime)
		
		
    },

});
