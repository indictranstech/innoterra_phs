import frappe
from frappe.model.mapper import get_mapped_doc

from frappe.utils import flt, getdate, nowdate



@frappe.whitelist()
def make_Sales_order(source_name, target_doc=None,ignore_permissions=False):

	# customer = _make_customer(source_name, ignore_permissions)
	# ordered_items = frappe._dict(
	# 	frappe.db.get_all(
	# 		"Sales Order Item",
	# 		{"prevdoc_docname": source_name, "docstatus": 1},
	# 		["item_code", "sum(qty)"],
	# 		group_by="item_code",
	# 		as_list=1,
	# 	)
	# )
	# def update_item(obj, target, source_parent):
	# 	balance_qty = obj.qty - ordered_items.get(obj.item_code, 0.0)
	# 	target.qty = balance_qty if balance_qty > 0 else 0
	# 	target.stock_qty = flt(target.qty) * flt(obj.conversion_factor)

	# 	if obj.against_blanket_order:
	# 		target.against_blanket_order = obj.against_blanket_order
	# 		target.blanket_order = obj.blanket_order
	# 		target.blanket_order_rate = obj.blanket_order_rate

	target_doc = get_mapped_doc("Purchase Order", source_name,
		{
			"Purchase Order": {
					"doctype": "Sales Order",
					"field_map": {
						# "status": "Pending For Delivery",
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
				# "postprocess": update_item,
				"condition": lambda doc: doc.qty > 0,
			
			} 											


			# "Purchase Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},

		
		}, target_doc)
 
	return target_doc