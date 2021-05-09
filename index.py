# -*- coding: utf-8 -*-
import sys
import csv
from collections import Counter

def get_orders_by_barcode(orders, barcode):
	result = []
	for order_id in orders.keys():
		b_list = orders[order_id][1]
		if barcode in b_list:
			result.append(order_id)
	return result

def process(path1, path2):
	orders = {}
	barcodes = []
	try:
		print("processing orders...")
		with open(path1, 'r') as f1:
			reader1 = csv.reader(f1, delimiter=',')
			next(reader1)
			for row in reader1:
				customer_id, order_id = map(int, row)
				orders[order_id] = [customer_id, []]
		print("processing barcodes...")
		with open(path2, 'r') as f2:
			reader2 = csv.reader(f2, delimiter=',')
			next(reader2)
			for row in reader2:
				barcode, order_id = row
				barcode = int(barcode)
				if order_id == '':
					order_id = None	
				else:
					order_id = int(order_id)
				if barcode in barcodes:
					print('Found barcode ({}) but already found in system.'.format(barcode))
				else:
					barcodes.append(barcode)
					if order_id:
						orders[order_id][1].append(barcode)
		# remove orders with no barcodes
		order_ids = []
		for order_id in orders.keys():
			if not orders[order_id][1]:
				order_ids.append(order_id)
		for order_id in order_ids:
			print('Order ({}) without barcodes. Removed from operations.'.format(order_id))
			del orders[order_id]
		print('generating file...')
		writeToFile(orders)
		# top 5 customers (most tickets) -- customer_id, amount tickets
		customers = {}
		for key in orders.keys():
			order = orders[key]
			customer_id, bcodes = order
			if customer_id not in customers:
				customers[customer_id] = len(bcodes)
			else:
				customers[customer_id] = customers[customer_id] + len(bcodes)
		#top_customers = {k: v for k, v in sorted(customers.items(), key=lambda item: item[1], reverse=True)}
		top_customers = dict(Counter(customers).most_common(5))
		print('printing top 5 customers...')
		for customer_id, amount in top_customers.items():
			print(customer_id, amount)
		# check unused
		unused = 0
		for barcode in barcodes:
			orders_by_bc = get_orders_by_barcode(orders, barcode)
			if not orders_by_bc:
				unused +=1 
		print('printing total unused barcodes: ', unused)
	except Exception as inst:
		print(inst)

def writeToFile(orders):
	csv_file = 'result.csv'
	csv_columns = ['customer_id','order_id','barcodes']
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for key in orders.keys():
				order = orders[key]
				writer.writerow({'customer_id': order[0], 'order_id': key, 'barcodes': order[1]})
	except IOError:
		print('I/O error')

if __name__ == '__main__':
	try:
		_ , path1, path2 = sys.argv
	except ValueError:
		print('We need 2 files as input.')
	else:
		process(path1, path2)
