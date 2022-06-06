# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Survey(Document):
	def validate(self):
		farmer_doc = frappe.get_doc("Supplier",self.name_of_farmer)
		address_doc = frappe.get_doc("Address",{'address_title':farmer_doc.supplier_name})
		self.village = address_doc.village
		self.tehsil = address_doc.taluka
		self.district = address_doc.county
		self.territory_name = address_doc.territory
		territory_doc = frappe.get_doc("Territory",address_doc.territory)
		self.territory_no =  territory_doc.territory_number
		

