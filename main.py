'''
Main File for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from visualize import Visualize
from retrieval import Retrieval
from helper import *
from change import Change
import sys

import os
import argparse

# DATA_FILE = './Expense_header_wrong.csv'
DATA_FILE = './Expense.csv'

def save_expense_entry(title, category, date, amount):
	''' 
	Append expense entry to a csv file
	Inputs :
		Title : String , description of the entry
		Category : Integer 1-6, as follows:
			- 1 : Groceries
			- 2 : Entertainment
			- 3 : Travel
			- 4 : Shopping
			- 5 : Bills
			- 6 : Investments
		Date : The date of the expense in DD-MM-YYYY format
		Amount : Float value (CHF)
		csv_file: the csv file to store all users' expense data
	Returns True if entry saved successfully, False otherwise
	'''
	entry_list = [title, category, date, amount]
	try:
		with open(DATA_FILE, 'a') as f:
		    writer = csv.writer(f)
		    writer.writerow(entry_list)
		return True 
	except:
		return False

def load_expenses():
	'''
	Load the expense csv file and
	return dataframe of entries
	'''
    # Checks if there is data to load, if there is not create a csv with the header
	try:
		print("load expense")
		df = pd.read_csv(DATA_FILE, header=0, encoding='UTF8')
		assert validate_column_names(df)

	except:
		# with open(DATA_FILE, 'w', newline='') as csv_file:
		# 	csv.writer(csv_file).writerow(['Title','Category','Date','Amount'])
		# df = pd.read_csv(DATA_FILE, header=0)
		df = pd.read_csv(DATA_FILE, names = ['Title','Category','Date','Amount'])
		sys.exit()

	# Check if every row has the right datatype
	if not validate_row_data(df):
		sys.exit()
    
	df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
	return df

def input_expense():
	'''
	Asks the user to provide titel, category, date and amount of a expense.
	Checks if the user input are in a format that we want
	'''
	print('Let\'s start adding Expenses')
	n_expense = input("How many expenses you want to enter?")
	for i in range(int(n_expense)):
		title = input('Enter the Title of the Expense: ')
		
		# Category input and error handling
		valid_category_flag = False
		while(not valid_category_flag):
			category = input_category()
			valid_category_flag = validate_category(category)
			if not valid_category_flag:
				print('Please enter a valid category between 1 and 6')

		# Date input and error handling
		valid_date_flag = False
		while(not valid_date_flag):
			date = input('Enter the Date of the Expense as DD-MM-YYYY(shortcut "t" for today): ')
			if date == "t":
				date = str(datetime.date.today().strftime('%d-%m-%Y'))
			valid_date_flag = validate_date(date)
			if not valid_date_flag:
				print('Please enter a valid date in DD-MM-YYYY Format')

		valid_amount_flag = False
		while(not valid_amount_flag):
			amount = input('Enter the Amount: ')
			valid_amount_flag, amount = validate_amount(amount)
			if not valid_amount_flag:
				print('Please enter a valid amount value')

		if save_expense_entry(title, category, date, amount):
			print("New expense ["+title+","+str(category)+","+date+","+str(amount)+"] successfully saved!")
			# print('Expense successfully saved!')
		else:
			print('Oops! We ran into some trouble. Please try again later')


def add(args):
	DATA_FILE = args.add[0]
	title = args.add[1]
	category = args.add[2]
	date = args.add[3]
	amount = args.add[4]


	print(title, category, date, amount)
	# Category input and error handling
	valid_category_flag = False
	valid_category_flag = validate_category(category)
	if not valid_category_flag:
		print("wrong category")
		sys.exit()

	# Date input and error handling
	valid_date_flag = False
	if date == "t":
		date = str(datetime.date.today().strftime('%d-%m-%Y'))
	valid_date_flag = validate_date(date)
	if not valid_date_flag:
		print('Please enter a valid date in DD-MM-YYYY Format')
		sys.exit()

	valid_amount_flag = False
	valid_amount_flag, amount = validate_amount(amount)
	if not valid_amount_flag:
		print('Please enter a valid amount value')

	# print(title, category, date, amount)

	if save_expense_entry(title, category, date, amount):
		print("New expense ["+title+","+str(category)+","+date+","+str(amount)+"] successfully saved!")
	else:
		print('Oops! We ran into some trouble. Please try again later')


if __name__ == '__main__':
	'''
	Asks the user what action the user wants to take when the code is executed.
	The choices are:
		1. Enter Expense Entry
		2. Filter Expenses
		3. Visualize Expenses
    Checks if the chosen choice is available.
	'''
	# CLI Implementation test
	# create parser object
	parser = argparse.ArgumentParser(description = "An Expense Tracker!")

	# defining arguments for parser object
	parser.add_argument("-a", "--add", type = str, nargs = 5, metavar = ('file_name','title', 'category', 'date', 'amount'), default = None, 
		help = "Add expense to tracker. \n\
				[file_name]: name of csv files. \n\
		   		[Category] : 1 : Groceries \n\
							2 : Entertainment \n\
							3 : Travel\n \
							4 : Shopping \n\
							5 : Bills\n \
							6 : Investments \n\
				[Dateformat]: DD-MM-YYYY (shortcut t for today)")
	args = parser.parse_args()

	if args.add != None:
		add(args)
	else:
		print('Welcome to Expense Tracker!')
		df = load_expenses()
		
		input_task_flag = False
		while not input_task_flag:
			print('What would you like to do today? \n \
				1. Enter Expense Entry \n \
				2. Filter Expenses \n \
				3. Visualize Expenses \n \
				4. Change Existing Entry \n')
			input_task = input('Please Enter the Number for the task you want to perform: ')
			
			# Input sanitisation
			try:
				input_task = int(input_task)
			except:
				print('Invalid Input!! Please enter a valid integer for the task')
				continue

			# Switch case of task options
			if input_task == 1: 
				input_expense()
				input_task_flag = True
			elif input_task == 2: 
				#filter_expenses(df)
				retrieval = Retrieval(df)
				input_task_flag = True
			elif input_task == 3:
				visualizer = Visualize(df)
				input_task_flag = True
			elif input_task == 4:
				change = Change(df)
				input_task_flag = True
			else:
				print('Invalid Input!! Please enter a valid integer for the task') 
