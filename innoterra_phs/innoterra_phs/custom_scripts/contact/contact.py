import frappe

def validate(doc, method=None):

    dtypes = [d.link_doctype for d in doc.links]

    if ("Customer" in dtypes) or ("Supplier" in dtypes):
        contacts = frappe.get_all("Contact Phone", {'parent':['!=', doc.name]}, "phone")
        nos = list({i.phone for i in contacts})
        nos_list = []
        for row in doc.phone_nos:
            if row.phone in nos or row.phone in nos_list:
                frappe.throw("Mobile No: %s already exists." % row.phone)
            nos_list.append(row.phone)
