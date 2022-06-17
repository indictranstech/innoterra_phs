// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warehouse Inspection', {
	refresh: function(frm) {
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Warehouse Inspection'};

		frm.toggle_display(['address_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
	

 },
 setup: function (frm) {
 	frm.set_query("warehouse_primary_address", function(doc) {
			return {
				query: "innoterra_phs.innoterra_phs.doctype.warehouse_inspection.warehouse_inspection.get_warehouse_primary_address",
				filters: {
					"warehouse": doc.name
				}
			};
		});
 },



	"year_of_construction": function (frm) {
		if (frm.doc.year_of_construction) {
			$(frm.fields_dict['age_warehouse_html'].wrapper).html(`${__('Age of the Warehouse')} : ${get_warehouse_age(frm.doc.year_of_construction)}`);
		} else {
			$(frm.fields_dict['age_warehouse_html'].wrapper).html('');
		}
	}
});

let get_warehouse_age = function (construction_year) {
	let ageMS = Date.parse(Date()) - Date.parse(construction_year);
	let age = new Date();
	age.setTime(ageMS);
	let years = age.getFullYear() - 1970;
	return years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
};
