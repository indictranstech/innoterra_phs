import frappe

def validate(doc, method=None):
    if doc.mobile_no:
        if frappe.db.exists("Supplier", {'supplier_name':doc.supplier_name, 'mobile_no':doc.mobile_no, 'is_farmer':1}):
            frappe.throw("Duplicate Values for Supplier Name and Mobile No.")
        if frappe.db.exists("Supplier", {'mobile_no':doc.mobile_no}):
            frappe.throw("Mobile Number already exists.")
