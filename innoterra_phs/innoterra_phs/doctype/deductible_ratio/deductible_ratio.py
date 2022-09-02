# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr,flt, nowdate



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