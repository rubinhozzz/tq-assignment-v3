# -*- coding: utf-8 -*-
import sys
import csv
from collections import Counter

class Barcode:
	def __init__(self, id, order_id=None):
		self.id = id
		self.order_id = order_id

class Order:
	def __init__(self, id, customer_id):
		self.id = id
		self.customer_id = customer_id
		self.barcodes = []

def get_order_by_id(orders, id):
	for order in orders:
		if order.id == id:
			return order
	return None

def validate_barcode(barcodes, barcode_id):
	barcode_ids = [b.id for b in barcodes]
	if barcode_id in barcode_ids:
		return False
	return True

def get_barcodes_by_order(barcodes, order_id):
	result = []
	for barcode in barcodes:
		if barcode.order_id == order_id:
			result.append(barcode)
	return result

def process(path1, path2):
	orders = []
	barcodes = []
	try:
		print("processing orders...")
		with open(path1, 'r') as f1:
			reader1 = csv.reader(f1, delimiter=',')
			next(reader1)
			for row in reader1:
				customer_id, order_id = map(int, row)
				order = Order(order_id, customer_id)
				orders.append(order)
		print("processing barcodes...")
		with open(path2, 'r') as f2:
			reader2 = csv.reader(f2, delimiter=',')
			next(reader2)
			for row in reader2:
				barcode_id, order_id = row
				barcode_id = int(barcode_id)
				if order_id == '':
					order_id = None	
				else:
					order_id = int(order_id)
				ok = validate_barcode(barcodes, barcode_id)
				if ok:
					barcode = Barcode(barcode_id, order_id)
					barcodes.append(barcode)
					if order_id:
						order = get_order_by_id(orders, order_id)
						order.barcodes.append(barcode)
				else:
					print('Found barcode ({}) but already found in system.'.format(barcode_id))
		#orders = [order for order in orders if order.barcodes]
		tmp_orders = []
		for order in orders:
			if order.barcodes:
				tmp_orders.append(order)
			else:
				print('Order ({}) without barcodes. Removed from operations.'.format(order.id))
		orders = tmp_orders
		print('generating file...')
		# writing to file
		writeToFile(orders)
		# top 5 customers (most tickets) -- customer_id, amount tickets
		customers = {}
		for order in orders:
			if order.customer_id not in customers:
				customers[order.customer_id] = len(order.barcodes)
			else:
				customers[order.customer_id] = customers[order.customer_id] + len(order.barcodes)
		top_customers = dict(Counter(customers).most_common(5))
		print('printing top 5 customers...')
		for customer_id, amount in top_customers.items():
			print(customer_id, amount)
		# check unused
		unused = 0
		for barcode in barcodes:
			if barcode.order_id == None:
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
			for order in orders:
				b_ids = [b.id for b in order.barcodes]
				writer.writerow({'customer_id': order.customer_id, 
								'order_id': order.id, 
								'barcodes': b_ids})
	except IOError:
		print('I/O error')

if __name__ == '__main__':
	try:
		_ , path1, path2 = sys.argv
	except ValueError:
		print('We need 2 files as input.')
	else:
		process(path1, path2)