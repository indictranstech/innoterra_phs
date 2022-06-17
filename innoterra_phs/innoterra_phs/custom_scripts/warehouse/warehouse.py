import frappe
import json
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,)

def onload(doc,method):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(doc)

def fetch_address(doc,method):
	ware_insp_doc = frappe.get_doc("Warehouse Inspection",doc.warehouse_inspection)
	values = {'warehouse':ware_insp_doc.name}
	address_list = frappe.db.sql(
		"""
		SELECT
			`tabAddress`.name from `tabAddress`,
			`tabDynamic Link`
		WHERE
			`tabAddress`.name = `tabDynamic Link`.parent
			and `tabDynamic Link`.link_name = %(warehouse)s
			and `tabDynamic Link`.link_doctype = 'Warehouse Inspection'
			
		""", values =values, as_dict=1)
	for address in address_list:
		addr_doc = frappe.get_doc("Address",address.name)
		addr_doc.append("links",{'link_doctype':'Warehouse','link_name':doc.name,'link_title':doc.name})
		addr_doc.save()

