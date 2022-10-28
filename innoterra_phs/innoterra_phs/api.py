import frappe

@frappe.whitelist()
def create_farmer_custom(data):
	try:
		details = frappe.parse_json(data)
		if frappe.db.exists("Customer", {'customer_name':details.get("customer_name")}):
			return "Duplicate Name Error - Customer {0} already exists".format(details.get("customer_name"))
		else:
			details.update({'doctype':"Customer"})
			doc = frappe.get_doc(details).insert()
			frappe.local.response.update({"data": doc.as_dict()})
			frappe.db.commit()
	except Exception as e:
		raise e		
