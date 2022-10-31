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

@frappe.whitelist()
def create_village_custom(data):
	try:
		details = frappe.parse_json(data)
		if frappe.db.exists("Village", {'village_name':details.get("village_name")}):
			return "Duplicate Name Error - Village {0} already exists".format(details.get("village_name"))
		else:
			details.update({'doctype':"Village"})
			doc = frappe.get_doc(details).insert()
			frappe.local.response.update({"data": doc.as_dict()})
			frappe.db.commit()
	except Exception as e:
		raise e

@frappe.whitelist()
def update_village(data):
	try:
		details = frappe.parse_json(data)
		village = frappe.db.exists("Village", {"village_id":details.get("village_id")})
		if village:
			doc = frappe.get_doc("Village", village, for_update=True)
			doc.update(details)
			frappe.local.response.update({"data": doc.save().as_dict()})
			frappe.db.commit()
		else:
			return "Village ID {0} does not exist.".format(details.get("village_id"))
	except Exception as e:
		raise e

@frappe.whitelist()
def update_taluka(data):
	try:
		details = frappe.parse_json(data)
		taluka = frappe.db.exists("Taluka", {"taluka_id":details.get("taluka_id")})
		if taluka:
			doc = frappe.get_doc("Taluka", taluka, for_update=True)
			doc.update(details)
			frappe.local.response.update({"data": doc.save().as_dict()})
			frappe.db.commit()
		else:
			return "Taluka ID {0} does not exist.".format(details.get("taluka_id"))
	except Exception as e:
		raise e

@frappe.whitelist()
def update_district(data):
	try:
		details = frappe.parse_json(data)
		district = frappe.db.exists("District", {"district_id":details.get("district_id")})
		if district:
			doc = frappe.get_doc("District", district, for_update=True)
			doc.update(details)
			frappe.local.response.update({"data": doc.save().as_dict()})
			frappe.db.commit()
		else:
			return "District ID {0} does not exist.".format(details.get("district_id"))
	except Exception as e:
		raise e

@frappe.whitelist()
def update_state(data):
	try:
		details = frappe.parse_json(data)
		state = frappe.db.exists("State", {"state_id":details.get("state_id")})
		if state:
			doc = frappe.get_doc("State", state, for_update=True)
			doc.update(details)
			frappe.local.response.update({"data": doc.save().as_dict()})
			frappe.db.commit()
		else:
			return "State ID {0} does not exist.".format(details.get("state_id"))
	except Exception as e:
		raise e
