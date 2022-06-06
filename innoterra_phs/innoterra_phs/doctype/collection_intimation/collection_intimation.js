// Copyright (c) 2022, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Collection Intimation', {
	 refresh: function(frm) {
	 	frm.add_custom_button("Create Quality Inspection", 
	 		() => frm.events.make_qi(frm)
        );

	 },
	 make_qi : function(frm) {
	 	console.log("inside make_qi")
	 	var dialog = new frappe.ui.Dialog({
			title: __("For Collection Items"),
			fields: [ 
				{fieldname: 'items_for_qc', fieldtype: 'Table', label: 'Select Items',
					fields: [
						{
							fieldtype:'Data',
							fieldname:'item_name',
							label: __('Item'),
							read_only:1,
							in_list_view:1
						},
						{
							fieldtype:'Datetime',
							fieldname:'date_of_collection',
							label: __('Collection Date'),
							read_only:1,
							in_list_view:1
						}
					],
					data: cur_frm.doc.collection_items,
					get_data: function() {
						return cur_frm.doc.collection_items
					}
				},

				{"fieldtype": "Button", "label": __('Create Quality Inspection'), "fieldname": "create_quality_inspection", "cssClass": "btn-primary"},

			],

		});
	 	dialog.fields_dict.create_quality_inspection.$input.click(function() {
			var data = dialog.get_values();
			//console.log("data===>",data)
			let selected_items = dialog.fields_dict.items_for_qc.grid.get_selected_children()
			// for(let i in selected_items){
			// 	console.log("selected_items==>",selected_items)
			// }
			if(selected_items.length == 0) {
				frappe.throw({message: 'Please select Item form Table for QC', title: __('Message'), indicator:'blue'})
			}
			let selected_items_list = []
			for(let i in selected_items){
				selected_items_list.push(selected_items[i].item_name)
			}			
			
			frappe.call({
				"method":"innoterra_phs.innoterra_phs.doctype.collection_intimation.collection_intimation.make_quality_inspection",
				"args":{
					"selected_items": selected_items_list,
					"doc" : frm.doc.name,
					"territory" : frm.doc.territory
				},
				callback:function(r){
					if(!r.exc) {
    					if(r.message) {
   							frappe.set_route('List', 'Quality Inspection', {"reference_name1": frm.doc.name })
                         }}
						}
        	   })
			    dialog.hide();
		});
		dialog.show();
}
 });





	 	