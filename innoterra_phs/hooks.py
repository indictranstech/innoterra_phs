from . import __version__ as app_version

app_name = "innoterra_phs"
app_title = "Innoterra Phs"
app_publisher = "Indictranstech"
app_description = "phs customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "nilima.d@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/innoterra_phs/css/innoterra_phs.css"
# app_include_js = "/assets/innoterra_phs/js/innoterra_phs.js"

# include js, css files in header of web template
# web_include_css = "/assets/innoterra_phs/css/innoterra_phs.css"
# web_include_js = "/assets/innoterra_phs/js/innoterra_phs.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "innoterra_phs/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "innoterra_phs.install.before_install"
# after_install = "innoterra_phs.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "innoterra_phs.uninstall.before_uninstall"
# after_uninstall = "innoterra_phs.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "innoterra_phs.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"innoterra_phs.tasks.all"
# 	],
# 	"daily": [
# 		"innoterra_phs.tasks.daily"
# 	],
# 	"hourly": [
# 		"innoterra_phs.tasks.hourly"
# 	],
# 	"weekly": [
# 		"innoterra_phs.tasks.weekly"
# 	]
# 	"monthly": [
# 		"innoterra_phs.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "innoterra_phs.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "innoterra_phs.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "innoterra_phs.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"innoterra_phs.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

doctype_js = {
	"Quality Inspection": "innoterra_phs/custom_scripts/quality_inspection/quality_inspection.js",
	"Purchase Order": "innoterra_phs/custom_scripts/purchase_order/purchase_order.js",
	"Purchase Receipt": "innoterra_phs/custom_scripts/purchase_receipt/purchase_receipt.js",
	"Purchase Invoice": "innoterra_phs/custom_scripts/purchase_invoice/purchase_invoice.js",
	"Sales Order": "innoterra_phs/custom_scripts/sales_order/sales_order.js",
	"Item Price": "innoterra_phs/custom_scripts/item_price/item_price.js"


}


doc_events = {
	"Quality Inspection":{
		"validate":"innoterra_phs.innoterra_phs.custom_scripts.quality_inspection.quality_inspection.validate_benchmark" },
	"Item Price" : {
	"validate" : "innoterra_phs.innoterra_phs.custom_scripts.item_price.item_price.validate_item_price",
	"before_save" : "innoterra_phs.innoterra_phs.custom_scripts.item_price.item_price.before_save_date"},
	 "Warehouse" : {
	 "after_insert" : "innoterra_phs.innoterra_phs.custom_scripts.warehouse.warehouse.fetch_address",
	 "onload": "innoterra_phs.innoterra_phs.custom_scripts.warehouse.warehouse.onload"}
}



fixtures = ['Custom Field', 'Property Setter', 'Print Format', 'Role', 'Letter Head', 'Print Style', 'Print Settings',"Workflow","Workflow State","Workflow Action","Terms and Conditions" ]
