# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Survey(Document):
	def validate(self):
		farmer_doc = frappe.get_doc("Supplier",self.name_of_farmer)
		if not frappe.db.exists("Address",{'address_title':farmer_doc.supplier_name}):
			frappe.throw("Address not found for farmer {0}".format(self.name_of_farmer))
		address_doc = frappe.get_doc("Address",{'address_title':farmer_doc.supplier_name})
		self.village = address_doc.village
		self.tehsil = address_doc.taluka
		self.district = address_doc.county
		self.territory_name = address_doc.territory
		if not address_doc.territory:
			frappe.throw("Cluster is not set on farmer address.")
		territory_doc = frappe.get_doc("Territory",address_doc.territory)
		self.territory_no =  territory_doc.territory_number
		
@frappe.whitelist()
def make_harvest_intimation(source_name):
	
	doc = get_mapped_doc("Survey", source_name, {
		"Survey": {
			"doctype": "Harvest Intimation",
			"field_map": {
					"name_of_farmer":"farmer",
					"name": "survey_reference",
					"cc_name": "cc_name"
				},
			"validation": {
					"docstatus": ["!=", 2]
				}
			},
		"Current Sowing Details": {
			"doctype": "Harvest Details",
			"field_map": {
				"crop": "item_name"
				},
			},
		})
	
	return doc
		

