# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.utils import cint, cstr,flt
import json



class CollectionIntimation(Document):
	def validate(self):
		farmer_doc = frappe.get_doc("Supplier",self.farmer)
		address_doc = frappe.get_doc("Address",{'address_title':farmer_doc.supplier_name})
		self.territory =address_doc.territory


# create quality inspection on clicking create quality inspection
@frappe.whitelist()
def make_quality_inspection(selected_items,doc,territory):
	print("inside make_quality_inspection")
	#item_value = json.loads(item_name)
	#item_name1 = item_value.get('item_name')
	if isinstance(selected_items, str):
		selected_items = json.loads(selected_items)
	
	for item in selected_items:
		qc_doc = frappe.new_doc("Quality Inspection")
		if qc_doc:
			qc_doc.reference_type1 = "Collection Intimation"
			qc_doc.reference_name1 = doc
			qc_doc.item_code = item
			qc_doc.inspection_type = "Incoming"
			qc_doc.inspected_by = "Administrator"
			qc_doc.sample_size = 0.0
			qc_doc.territory = territory
			qc_doc.flags.ignore_mandatory = True
			qc_doc.save()
		else:
			frappe.throw("Please Select Atleast One Item")
	return qc_doc.name