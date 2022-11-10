# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

from lib2to3.pgen2 import driver
import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr,flt, nowdate
from frappe.model.mapper import get_mapped_doc
from innoterra_phs.innoterra_phs.custom_scripts.purchase_order.purchase_order import get_warehouse_address

from frappe.utils import today


class DeductibleRatio(Document):
	# calculations for difference and offer price 
	def validate(self):
		diff_sum = 0
		diff_qty = 0
		for item in self.quality_inspection_parameter_benchmark:
			if item.deductible_ratio_trigger == 'Greater Than':
				if item.actual_quality_inspection > item.benchmark_value:
					item.difference = flt(item.multiplier*(item.actual_quality_inspection - item.benchmark_value))
					item.difference_qty = flt(item.actual_quality_inspection - item.benchmark_value)

				else :
					item.difference = 0
					item.difference_qty = 0

			else :
				if item.actual_quality_inspection < item.benchmark_value :
					item.difference = flt(item.multiplier*(item.benchmark_value - item.actual_quality_inspection))
					item.difference_qty = flt(item.benchmark_value - item.actual_quality_inspection)

				else :
					item.difference = 0
					item.difference_qty = 0

			diff_sum = diff_sum + item.difference
			diff_qty = diff_qty + item.difference_qty

		self.deduction_amount = diff_sum
		self.deduction_qty = diff_qty

		ans = flt(self.deduction_amount/100)
		per = flt(self.deduction_qty/100)

		self.offer_priced = self.agreed_price - (self.agreed_price * ans)
		self.offer_qty = self.agreed_qty - (self.agreed_qty * per)
		
# adding item price into item price list 
@frappe.whitelist()
def add_pricelist(item,rate,price_list):
	if not frappe.db.exists("Item Price",{'item_code':item,'price_list':price_list}):
		price_doc = frappe.new_doc("Item Price")
		if price_doc:
			price_doc.item_code = item
			price_doc.price_list = price_list
			price_doc.price_list_rate = rate
			price_doc.save()

			#frappe.db.commit()
		else:
			frappe.throw("price list not created")
	
	else :
		old_price_doc = frappe.get_doc("Item Price",{'item_code':item,'price_list':price_list})
		if old_price_doc:
			frappe.db.set_value("Item Price",old_price_doc.name,'valid_upto',nowdate())
			frappe.db.commit()

		price_doc = frappe.new_doc("Item Price")
		if price_doc:
			price_doc.item_code = item
			price_doc.price_list = price_list
			price_doc.price_list_rate = rate
			price_doc.save()

			#frappe.db.commit()
		else:
			frappe.throw("price list not created")
	
	return price_doc.name

@frappe.whitelist()
def Create_Qty_PO(source_name):
	doc = frappe.get_doc('Deductible Ratio',source_name)
	itemscode = frappe.get_doc("Item",doc.item_code)
	item = []
	item.append(
		{
				"item_code": itemscode.item_code,
				"item_name": itemscode.item_name,
				"description": itemscode.description,
				"item_group": itemscode.item_group,
				"qty": doc.offer_qty,
				"rate":doc.agreed_price,
				"amount":doc.offer_qty * doc.agreed_price,
				"base_amount": doc.offer_qty * doc.agreed_price,
				"net_rate": doc.agreed_price,
				"net_amount": doc.offer_qty * doc.agreed_price,
				"base_net_rate":doc.agreed_price,
				"base_net_amount":doc.offer_qty * doc.agreed_price,
				"doctype": "Purchase order Item",
			}
		
		)
	warehouse = get_warehouse(doc.qi_reference) if doc.qi_reference else ""
	wh_add = get_warehouse_address(warehouse) if warehouse else ""
	po = frappe.get_doc(
	{
	
		"supplier": doc.supplier_name,
		"conversion_rate": 1,
		"schedule_date":today(),
		"tax_category": "",
		"status": "Draft",
		"set_warehouse": warehouse or "",
		"shipping_address": wh_add.get("warehouse_address") if wh_add else "",
		"doctype": "Purchase Order",
		"items": item,
	}
		
	).insert()

	return po.name


@frappe.whitelist()
def Create_price_PO(source_name):
	doc = frappe.get_doc('Deductible Ratio',source_name)
	itemscode = frappe.get_doc("Item",doc.item_code)
	
	Revised_Price  = frappe.db.sql(f"""  select * from `tabRevised Price Table`  where parent ='{source_name}' and  price_list = 'Standard Buying'  """,as_dict=1)
	rp = float(Revised_Price[0]['revised_price'])

	item = []
	item.append(
		{
				"item_code": itemscode.item_code,
				"item_name": itemscode.item_name,
				"description": itemscode.description,
				"item_group": itemscode.item_group,
				"qty": doc.agreed_qty,
				"rate":rp,
				"amount":doc.agreed_qty * rp,
				"base_amount": doc.agreed_qty * rp,
				"net_rate": rp,
				"net_amount": doc.agreed_qty * rp,
				"base_net_rate":rp,
				"base_net_amount":doc.agreed_qty * rp,
				"doctype": "Purchase order Item",
			}
		
		)
	warehouse = get_warehouse(doc.qi_reference) if doc.qi_reference else ""
	wh_add = get_warehouse_address(warehouse) if warehouse else ""
	po = frappe.get_doc(
	{
	
		"supplier": doc.supplier_name,
		"conversion_rate": 1,
		"schedule_date":today(),
		"tax_category": "",
		"status": "Draft",
		"set_warehouse": warehouse or "",
		"shipping_address": wh_add.get("warehouse_address") if wh_add else "",
		"doctype": "Purchase Order",
		"items": item,
	}
		
	).insert()

	return po.name

def get_warehouse(qi_ref):
	#qi = frappe.db.get_value("Deductible Ratio", dr_doc, "qi_reference")
	ci = frappe.db.get_value("Quality Inspection", qi_ref, "reference_name1")
	wh = frappe.db.get_value("Collection Intimation", ci, "warehouse") if ci else ""
	if wh:
		return wh
