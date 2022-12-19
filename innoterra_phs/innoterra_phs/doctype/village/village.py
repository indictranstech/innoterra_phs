# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Village(Document):
	
	def validate(self, method=None):
		if frappe.db.exists("Village", {'village_name':self.village_name, 'taluka':self.taluka, 'district':self.district, 'state':self.state, 'cluster':self.cluster}):
			frappe.throw("Village already exists! (State-{0}, District-{1}, Taluka-{2}, Village-{3})".format(self.state, self.district, self.taluka, self.village_name))
		if self.state and not frappe.db.exists("State", self.state):
			frappe.throw("State {0} does not exist".format(self.state))
		if self.district and not frappe.db.exists("District", self.district):
			frappe.throw("District {0} does not exist".format(self.district))
		if self.taluka and not frappe.db.exists("Taluka", self.taluka):
			frappe.throw("Taluka {0} does not exist".format(self.taluka))
