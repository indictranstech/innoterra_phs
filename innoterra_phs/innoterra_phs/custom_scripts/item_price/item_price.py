import frappe
from frappe.utils import nowdate
from datetime import datetime
from frappe.utils import today

# valid from date should not be past date 
def validate_item_price(doc,method):
	if doc.docstatus!=1 and doc.valid_from < nowdate():
		frappe.throw("Valid From should not be past date")


def before_save_date(doc,method):
	if not doc.valid_from:
		doc.valid_from = nowdate()
	if not frappe.db.exists("Item Price",{'item_code':doc.item_code,'price_list':doc.price_list}):
		return
	else :
		old_price_doc = frappe.get_doc("Item Price",{'item_code':doc.item_code,'price_list':doc.price_list})
		if old_price_doc:
			frappe.db.set_value("Item Price",old_price_doc.name,'valid_upto',nowdate())
			frappe.db.commit()
		else:
			frappe.throw("valid_upto is not updated")

@frappe.whitelist()
def upate_po(item_code,name,sd,ed):
	if ed == None or ed == "":
		ed = today()

	item_price = frappe.get_doc("Item Price",name)
	dd = frappe.db.sql(f""" 
				select 
				po.name poname
				from `tabPurchase Order` po 
				
				left join `tabPurchase Order Item` poi on po.name = poi.parent
				
				where po.workflow_state = 'Pending to Receive'
					and 
					poi.item_code = '{item_code}'
					and
					po.transaction_date between '{sd}' and '{ed}' 
		""",as_dict=1) 
		
	for i in dd:
		po = frappe.get_doc("Purchase Order",i['poname'])
		for j in po.items:
			if j.item_code == item_code:
				frappe.db.set_value('Purchase Order Item',j.name,{"rate" :item_price.price_list_rate})
				j.rate = item_price.price_list_rate
				j.base_rate = item_price.price_list_rate
				j.net_rate = item_price.price_list_rate
		po.save()
		frappe.db.commit()
	return 'done'


	  
