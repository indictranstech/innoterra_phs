import frappe
from frappe.utils import nowdate
from datetime import datetime

# valid from date should not be past date 
def validate_item_price(doc,method):
	if doc.valid_from < nowdate():
		frappe.throw("Valid From should not be past date")


def before_save_date(doc,method):
	if not frappe.db.exists("Item Price",{'item_code':doc.item_code,'price_list':doc.price_list}):
		return
	else :
		old_price_doc = frappe.get_doc("Item Price",{'item_code':doc.item_code,'price_list':doc.price_list})
		if old_price_doc:
			frappe.db.set_value("Item Price",old_price_doc.name,'valid_upto',nowdate())
			frappe.db.commit()
		else:
			frappe.throw("valid_upto is not updated")

