# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,)


class WarehouseInspection(Document):
	def validate(self):
		self.area_of_the_warehouse_sq_ft = flt(self.length_of_the_warehouse_ft) * flt(self.breadth_of_the_warehouse_ft)

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def on_update(self):
		self.create_primary_address()
		

	def create_primary_address(self):
		from frappe.contacts.doctype.address.address import get_address_display

		from erpnext.selling.doctype.customer.customer import make_address

		if self.flags.is_new_doc and self.get("address_line1"):
			address = make_address(self)
			address_display = get_address_display(address.name)

			self.db_set("warehouse_primary_address", address.name)
			self.db_set("primary_address", address_display)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_warehouse_primary_address(doctype, txt, searchfield, start, page_len, filters):
	warehouse = filters.get("warehouse")
	return frappe.db.sql(
		"""
		SELECT
			`tabAddress`.name from `tabAddress`,
			`tabDynamic Link`
		WHERE
			`tabAddress`.name = `tabDynamic Link`.parent
			and `tabDynamic Link`.link_name = %(warehouse)s
			and `tabDynamic Link`.link_doctype = 'Warehouse Inspection'
			and `tabAddress`.name like %(txt)s
		""",
		{"warehouse": warehouse, "txt": "%%%s%%" % txt},
	)



