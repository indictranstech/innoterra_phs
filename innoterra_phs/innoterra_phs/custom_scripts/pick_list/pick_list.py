import frappe
from frappe.utils import flt
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_pick_list(source_name, target_doc=None):
	from erpnext.stock.doctype.packed_item.packed_item import is_product_bundle

	def update_item_quantity(source, target, source_parent) -> None:
		picked_qty = flt(source.picked_qty) / (flt(source.conversion_factor) or 1)
		qty_to_be_picked = flt(source.qty) - max(picked_qty, flt(source.delivered_qty))

		target.qty = qty_to_be_picked
		target.stock_qty = qty_to_be_picked * flt(source.conversion_factor)

	def update_packed_item_qty(source, target, source_parent) -> None:
		qty = flt(source.qty)
		for item in source_parent.items:
			if source.parent_detail_docname == item.name:
				picked_qty = flt(item.picked_qty) / (flt(item.conversion_factor) or 1)
				pending_percent = (item.qty - max(picked_qty, item.delivered_qty)) / item.qty
				target.qty = target.stock_qty = qty * pending_percent
				return

	def should_pick_order_item(item) -> bool:
		return (
			abs(item.delivered_qty) < abs(item.qty)
			and item.delivered_by_supplier != 1
			and not is_product_bundle(item.item_code)
		)

	doc = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {"doctype": "Pick List", "validation": {"docstatus": ["=", 1]}},
			"Sales Order Item": {
				"doctype": "Pick List Item",
				"field_map": {"parent": "sales_order", "name": "sales_order_item"},
				"postprocess": update_item_quantity,
				"condition": should_pick_order_item,
			},
			"Packed Item": {
				"doctype": "Pick List Item",
				"field_map": {
					"parent": "sales_order",
					"name": "sales_order_item",
					"parent_detail_docname": "product_bundle_item",
				},
				"field_no_map": ["picked_qty"],
				"postprocess": update_packed_item_qty,
			},
		},
		target_doc,
	)

	doc.purpose = "Delivery"

	#doc.set_item_locations()

	return doc