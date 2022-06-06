# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate




class GatePass(Document):
	def validate(self):
		if self.dl_end_date == nowdate():
			frappe.throw("DL End Date should not Today's Date")
	


	
	

