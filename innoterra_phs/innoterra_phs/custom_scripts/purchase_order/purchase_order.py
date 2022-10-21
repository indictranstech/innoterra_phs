import frappe
from frappe.model.mapper import get_mapped_doc

from frappe.utils import flt, getdate, nowdate

@frappe.whitelist()
def get_warehouse_address(warehouse):
	wh_add = frappe.get_all("Dynamic Link", {'parenttype':"Address", 'link_doctype':"Warehouse", 'link_name':warehouse}, "parent")
	
	for add in wh_add:
		if frappe.db.get_value("Address", add.parent, "is_shipping_address"):
			return {'warehouse_address': add.parent}

@frappe.whitelist()
def make_Sales_order(source_name, target_doc=None,ignore_permissions=False):
	target_doc = get_mapped_doc("Purchase Order", source_name,
		{
			"Purchase Order": {
					"doctype": "Sales Order",
					"field_map": {
						"farmer_details": "farmer_details",
						"purchase_order":"name",
						"po_number":'',
						"inter_company_order_reference":''
					}
				},
			"Purchase Order Item":{
				"doctype": "Sales Order Item",
				"field_map": {
					"docstatus": 1,
					"delivery_by_supplier": 0,
					"prevdoc_docname":'',
					"warehouse":"warehouse"
					},
				"condition": lambda doc: doc.qty > 0,
			
			} 											
		
		}, target_doc)
 
	return target_doc
