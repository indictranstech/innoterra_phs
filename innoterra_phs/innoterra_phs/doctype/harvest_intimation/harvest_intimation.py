# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class HarvestIntimation(Document):
	pass

@frappe.whitelist()
def make_collection_intimation(source_name):
	
	doc = get_mapped_doc("Harvest Intimation", source_name, {
		"Harvest Intimation": {
			"doctype": "Collection Intimation",
			"field_map": {
					"farmer":"farmer",
					"name": "harvest_intimation_reference",
					"cc_name": "warehouse"
				},
			"validation": {
					"docstatus": ["!=", 2]
				}
			},
		"Harvest Details": {
			"doctype": "Collection Intimation Item",
			"field_map": {
				"item_name": "item_name"
				},
			},
		})
	
	return doc
