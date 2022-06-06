# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class WeighmentSheet(Document):
	def validate(self):
		sum = 0.0
		for item in self.weighment_details:
			sum += item.weight
		self.total_weight = sum

