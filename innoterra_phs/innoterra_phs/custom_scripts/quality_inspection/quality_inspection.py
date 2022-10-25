import frappe
from frappe.utils import cint, cstr,flt

# adding benchmark values in reading table
def validate_benchmark(doc,method):
	doc.flags.ignore_mandatory = True
	if doc.quality_inspection_template:

		for item in doc.readings:
			bench_doc = frappe.get_doc("Quality Inspection Rule Benchmarks",{'quality_inspection_parameter':item.specification, 'item_name':doc.item_code,'territory':doc.territory})
			item.benchmark = bench_doc.benchmark
			


# making deductible ratio document onckiking create deductible ratio button
@frappe.whitelist()
def make_deductible_ratio(doc):
	qc_doc = frappe.get_doc("Quality Inspection",doc)
	if qc_doc.readings:
		dr_doc = frappe.new_doc("Deductible Ratio")
		if dr_doc:
			dr_doc.item_code = qc_doc.item_code
			dr_doc.agreed_price = qc_doc.agreed_price
			dr_doc.agreed_qty = qc_doc.agreed_qty
			dr_doc.territory = qc_doc.territory
			dr_doc.qi_reference = qc_doc.name
			coll_doc = frappe.get_doc("Collection Intimation",qc_doc.reference_name1)
			dr_doc.supplier_name = coll_doc.farmer
			for item in qc_doc.readings:
				quality_rule_doc = frappe.get_doc("Quality Inspection Rule Benchmarks",{'quality_inspection_parameter':item.specification, 'item_name':qc_doc.item_code,'territory':qc_doc.territory})

				dr_doc.append("quality_inspection_parameter_benchmark",{
					'quality_inspection_parameters': quality_rule_doc.quality_inspection_parameter,
					'uom': quality_rule_doc.uom,
					'deductible_ratio_trigger':quality_rule_doc.deductible_ratio_trigger,
					'multiplier': quality_rule_doc.multiplier,
					'benchmark_value': quality_rule_doc.benchmark,
					'actual_quality_inspection':flt(item.get('reading_1'))
				})
			dr_doc.save()
		else:
			frappe.throw("new Deductible Ratio document not created")
	else:
		frappe.throw("Please Select Quality Inspection Template")
	return dr_doc.name




