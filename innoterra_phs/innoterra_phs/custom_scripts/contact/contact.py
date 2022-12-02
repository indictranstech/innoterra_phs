import frappe

def validate(doc, method=None):

    dtypes = [d.link_doctype for d in doc.links]

    if ("Customer" in dtypes) or ("Supplier" in dtypes):
        contacts = frappe.get_all("Contact Phone", ["parent","phone"])
        old_doc = doc.get_doc_before_save()
        doc_nos = [i.phone for i in old_doc.phone_nos]
        nos = list({i.phone for i in contacts})
        for row in doc.phone_nos:
            if row.phone in nos and row.phone not in doc_nos:
                frappe.throw("Mobile No: %s already exists." % row.phone)
