# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data

# Copyright (c) 2022, Indictranstech and contributors
# For license information, please see license.txt

from collections import defaultdict
import frappe
from frappe import _
from frappe.utils.data import flt



def execute(filters=None):
	condition = get_conditions(filters)
	columns = get_columns(filters)
	data = get_data(filters, condition)
	return columns, data


def get_columns(filters):
	"""return columns"""
	columns = [
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "width": 150},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 100,
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 100,
		},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 90,
		},
		{
			"label": _("Balance Qty"),
			"fieldname": "bal_qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty",
		},
		{
			"label": _("Balance Value"),
			"fieldname": "bal_val",
			"fieldtype": "Currency",
			"width": 100,
			"options": "currency",
		},
		{
			"label": _("Balance Bags"),
			"fieldname": "bal_bag",
			"fieldtype": "Float",
			"width": 100,
			
		},
		{
			"label": _("In Qty"),
			"fieldname": "in_qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty",
		},
		{
			"label": _("In Value"),
			"fieldname": "in_val",
			"fieldtype": "Currency",
			"width": 110,
			"options": "currency",
		},
		{
			"label": _("In Bags"),
			"fieldname": "in_bag",
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"label": _("Out Qty"),
			"fieldname": "out_qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty",
		},
		{
			"label": _("Out Value"),
			"fieldname": "out_val",
			"fieldtype": "Currency",
			"width": 110,
			"options": "currency",
		},
		{
			"label": _("Out Bags"),
			"fieldname": "out_bag",
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "rate",
			"fieldtype": "Currency",
			"width": 90,
			"convertible": "rate",
			"options": "currency",
		},
	]
	return columns

def get_conditions(filters):

	# print("this is conditions")
	conditions = ""
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))

	if not filters.get("to_date"):
		frappe.throw(_("'To Date' is required"))

	if filters.get("to_date") < filters.get("from_date"):
		frappe.throw(_(" 'To Date' should be after 'From Date' "))
		
	if filters.get("from_date") and filters.get("to_date"):
		conditions += """ and tpr.posting_date between '{0}' and '{1}'
		and tso.posting_date between '{0}' and '{1}'
		""".format(filters.get("from_date"), filters.get("to_date"))

	if filters.get("item_group"):
		conditions += " and tpri.item_group = '{0}' ".format(filters.get("item_group"))	

	if filters.get("item_code"):
		conditions += " and tpri.item_code = '{0}' ".format(filters.get("item_code"))

	if filters.get("warehouse"):
		conditions += " and tpri.warehouse = '{0}' ".format(filters.get("warehouse"))

	if filters.get("include_uom"):
		conditions += " and tpri.stock_uom = '{0}' ".format(filters.get("include_uom"))

	if filters.get("company"):
		conditions += " and tpr.company = '{0}'".format(filters.get("company"))	
		conditions += " and tso.company = '{0}'".format(filters.get("company"))	
		

	return conditions

def get_data(filters, conditions):
	
	new_condition = ""

	if filters.get("company"):
		new_condition += " and company = '{0}'".format(filters.get("company"))

	if filters.get("from_date") and filters.get("to_date"):
		new_condition += """ and posting_date between '{0}' and '{1}'
		""".format(filters.get("from_date"), filters.get("to_date"))

	if filters.get("item_code"):
		new_condition += " and item_code = '{0}' ".format(filters.get("item_code"))
		# main_condition += " and tpri.item_code = '{0}' ".format(filters.get("item_code"))

	if filters.get("warehouse"):
		new_condition += " and warehouse = '{0}' ".format(filters.get("warehouse"))

	if filters.get("include_uom"):
		new_condition += " and stock_uom = '{0}' ".format(filters.get("include_uom"))
				
	new_data = frappe.db.sql("""
					Select item_code, stock_uom,
					warehouse,
					GROUP_CONCAT(DISTINCT
					CASE 
						when voucher_type = "Purchase Receipt" then voucher_detail_no  
					END) as `pr_item`,
					GROUP_CONCAT(DISTINCT
					CASE 
						when voucher_type = "Purchase Invoice" then voucher_detail_no  
					END) as `pr_item`,
					GROUP_CONCAT(DISTINCT
					CASE 
						when voucher_type = "Sales Invoice" then voucher_detail_no  
					END) as `si_item`,
					GROUP_CONCAT(DISTINCT
					CASE 
						when voucher_type = "Delivery Note" then voucher_detail_no  
					END) as `dn_item`,
					GROUP_CONCAT(
					CASE 						
						when actual_qty < 0 and voucher_type in ('Purchase Invoice', 'Purchase Receipt', 'Sales Invoice', 'Delivery Note') 
						then actual_qty
						else 0
					END) as out_qty,					
					GROUP_CONCAT(
					CASE 
						when actual_qty > 0 and voucher_type in ('Purchase Invoice', 'Purchase Receipt', 'Sales Invoice', 'Delivery Note')
						then actual_qty
						else 0
					END) as in_qty,
					valuation_rate 
					from `tabStock Ledger Entry`
					where is_cancelled = 0
					{0}
					group by item_code, warehouse 
					order by posting_date,posting_time 		
				""".format(new_condition), as_dict=1)
	main_list = []
	if new_data:
		for n in new_data:
			
			in_bags = 0
			out_bags = 0
			if n.get("pr_item"):
				purchase_receipt = n.get("pr_item").split(",")
				for pr in purchase_receipt:
					in_bags += frappe.get_value("Purchase Receipt Item", pr, "count_of_bells_or_bags") 	

			if n.get("dn_item"):
				delivery_note = n.get("dn_item").split(",")
				for dn in delivery_note:
					out_bags += frappe.get_value("Delivery Note Item", dn, "count_of_bells_or_bags") 

			if n.get("pi_item"):
				purchase_invoice = n.get("pr_item").split(",")
				for pi in purchase_invoice:
					in_bags += frappe.get_value("Purchase Invoice Item", pi, "count_of_bells_or_bags") 	

			if n.get("si_item"):
				sales_invoices = n.get("dn_item").split(",")
				for si in sales_invoices:
					out_bags += frappe.get_value("Sales Invoice Item", si, "count_of_bells_or_bags") 		

			in_qty = abs(sum(float(x) for x in n.get("in_qty").split(",")))
			out_qty = abs(sum(float(x) for x in n.get("out_qty").split(",")))
			
			item = frappe.get_doc("Item", n.item_code)							
			main_list.append({
				"item_code":n.item_code,
				"item_name": item.item_name,
				"item_group": item.item_group,
				"warehouse":n.warehouse,
				"stock_uom": n.stock_uom,
				"in_qty": in_qty,
				"out_qty": out_qty,
				"in_bag": in_bags,
				"out_bag": out_bags,
				"in_val": (in_qty * n.valuation_rate),
				"out_val": (out_qty * n.valuation_rate),
				"rate": n.valuation_rate,
				"bag_balance": (in_bags - out_bags) if (in_bags - out_bags) > 0 else 0,
				"bal_bag": (in_bags - out_bags) if (in_bags - out_bags)> 0 else 0 ,
				"bal_qty": (in_qty - out_qty) if (in_qty - out_qty) > 0 else 0,
				"bal_val": (in_qty - out_qty)* n.valuation_rate if (in_qty - out_qty) > 0 else 0,
			})
	return main_list

