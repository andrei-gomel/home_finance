from prettytable import PrettyTable

def convert_payments(payments):
	all_payments = []
	for item in payments:
	    simple = (item["id"], item.get("data"), item["name"], item["price"])
	    all_payments.append(simple)
	return all_payments


def output_payments(payments):
	table = PrettyTable()
	table.field_names = payments[0].keys()
	for emp in payments:
	    table.add_row(emp.values())
	print(table)