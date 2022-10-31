# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class District(Document):
	
	def validate(self, method=None):
		
		if self.state and not frappe.db.exists("State", self.state):
			frappe.throw("State {0} does not exist".format(self.state))
