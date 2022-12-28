import frappe

def validate(doc, method=None):
	
	if doc.mobile_no and frappe.db.exists("Customer", {'name':["!=", doc.name], 'mobile_no':doc.mobile_no, 'customer_name':doc.customer_name}):
		frappe.throw("Duplicate Values for Customer name and Mobile No")
	if doc.mobile_no and doc.customer_group=="Farmer" and frappe.db.exists("Customer", {'mobile_no':doc.mobile_no, 'customer_group':"Farmer"}):
		frappe.throw("Mobile Number exists.")
