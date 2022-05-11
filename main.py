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
	df = pd.read_csv(DATA_FILE, header=0)
	df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
	return df


# def filter_expenses(df):
# 	'''
# 	Present options to the 
# 	user on the basis of which
# 	filter task to perform
# 	Options:
# 	1. By Date
# 	2. By Month
# 	3. By a window (Start/End Date)
# 	4. By Category
# 	'''
# 	input_filter_expense_flag = False
# 	while not input_filter_expense_flag:
# 		input_filter_expense = input('Please enter how you would like to filter the expenses, \n \
# 			Options are : \n \
# 			1. By Date \n \
# 			2. By Month \n \
# 			3. By Year \n \
# 			4. By a window (Start/End Date) \n \
# 			5. By Category \n \
# 			Enter Option: ')
		
# 		# Input sanitisation
# 		try:
# 			input_filter_expense = int(input_filter_expense)
# 		except:
# 			print('Invalid Input!! Please enter a valid integer for the task')
# 			continue

# 		# Code block for filtering expenses by a Date
# 		if input_filter_expense == 1:
# 			valid_date_flag = False
# 			while not valid_date_flag:
# 				date = input('Enter the Date as DD-MM-YYYY: ')
# 				valid_date_flag = validate_date(date)
# 				if not valid_date_flag:
# 					print('Please enter a valid date in DD-MM-YYYY Format')
# 				else:
# 					datetime_date = datetime.strptime(date, '%d-%m-%Y')
# 					df_filter = filter_expenses_by_date(df, datetime_date)
# 					print(f'Expenses on %s are: ' % datetime_date.strftime('%d %b, %Y'))
# 					print(df_filter)
# 			input_filter_expense_flag = True
# 		# Code block for filtering expenses by month
# 		elif input_filter_expense == 2:
# 			valid_month_flag = False
# 			while not valid_month_flag:
# 				month = input('Enter the Month as MM-YYYY: ')
# 				valid_month_flag = validate_month(month)
# 				if not valid_month_flag:
# 					print('Please enter a valid month in MM-YYYY Format')
# 				else:
# 					datetime_month = datetime.strptime(month, '%m-%Y')
# 					df_filter = filter_expenses_by_month(df, datetime_month)
# 					print(f'Expenses on %s are: ' % datetime_month.strftime('%b, %Y'))
# 					print(df_filter)
# 			input_filter_expense_flag = True

# 		# Code block for filtering expenses by year
# 		elif input_filter_expense == 3:
# 			valid_year_flag = False
# 			while not valid_year_flag:
# 				year = input('Enter the Year as YYYY: ')
# 				valid_year_flag = validate_year(year)
# 				if not valid_year_flag:
# 					print('Please enter a valid month in YYYY Format')
# 				else:
# 					datetime_year = datetime.strptime(year, '%Y')
# 					df_filter = filter_expenses_by_year(df, datetime_year)
# 					print(f'Expenses on %s are: ' % datetime_year.strftime('%Y'))
# 					print(df_filter)
# 			input_filter_expense_flag = True

# 		# Code block for filtering expenses by window
# 		elif input_filter_expense == 4:
# 			valid_date_flag = False
# 			while not valid_date_flag:
# 				start_date = input('Enter the Start Date as DD-MM-YYYY: ')
# 				end_date = input('Enter the End Date as DD-MM-YYYY: ')
# 				valid_date_flag = validate_date(start_date) & validate_date(end_date)
# 				if not valid_date_flag:
# 					print('Please enter a valid date in DD-MM-YYYY Format')
# 				else:
# 					datetime_start_date = datetime.strptime(start_date, '%d-%m-%Y')
# 					datetime_end_date = datetime.strptime(end_date, '%d-%m-%Y')
# 					df_filter = filter_expenses_by_timeframe(df, datetime_start_date, \
# 																	datetime_end_date)
# 					print(f'Expenses within %s and %s are: ' % (datetime_start_date.strftime('%d %b, %Y'),
# 																datetime_end_date.strftime('%d %b, %Y'))
# 						)
# 					print(df_filter)
# 			input_filter_expense_flag = True
# 		# Code block for filtering expenses by Category
# 		elif input_filter_expense == 5:
# 			valid_category_flag = False
# 			while(not valid_category_flag):
# 				category = input_category()
# 				valid_category_flag = validate_category(category)
# 				if not valid_category_flag:
# 					print('Please enter a valid category between 1 and 6')
# 				else:
# 					category = int(category)
# 					df_filter = filter_expenses_by_category(df, category)
# 					print(f'Expenses with Category %d are: ' % category)
# 					print(df_filter)
# 			input_filter_expense_flag = True
# 		else :
# 			print('Please enter a valid filter task')
# 	return 0


# def filter_expenses_by_date(df, date):
# 	'''
# 	Filter entries by input date
# 	and return the filtered Dateframe
# 	'''
# 	return df[df['Date'] == date.strftime('%Y-%m-%d')]


# def filter_expenses_by_month(df, datetime_month):
# 	'''
# 	Filter entries by input month
# 	and return the filtered Dateframe
# 	'''
# 	first_day = datetime_month.strftime("%Y-%m-01")
# 	last_day = datetime_month.strftime("%Y-%m-31") # it doesn't matter if the month has less than 31 days.
# 	return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]


# def filter_expenses_by_year(df, datetime_year):
# 	'''
# 	Filter entries by input year
# 	and return the filtered Dateframe
# 	'''
# 	first_day = datetime_year.strftime("%Y-01-01")
# 	last_day = datetime_year.strftime("%Y-12-31") 
# 	return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]


# def filter_expenses_by_timeframe(df, start_date, end_date):
# 	'''
# 	Filter entries by input
# 	start and end date
# 	Returns the filtered Dataframe
# 	'''
# 	start_date_f = start_date.strftime('%Y-%m-%d')
# 	end_date_f = end_date.strftime('%Y-%m-%d')
# 	return 	df[(df['Date'] >= start_date_f) & (df['Date'] <= end_date_f)]


# def filter_expenses_by_category(df, category):
# 	'''
# 	Filter entries by 
# 	Category and return the 
# 	filtered Dataframe 
# 	'''
# 	return df[df['Category'] == category]



def input_expense():
	print('Let\'s start adding Expenses')
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
		date = input('Enter the Date of the Expense as DD-MM-YYYY: ')
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
		print('Expense successfully saved!')
	else:
		print('Oops! We ran into some trouble. Please try again later')


if __name__ == '__main__':
	print('Welcome to Expense Tracker!')
	df = load_expenses()
	
	input_task_flag = False
	while not input_task_flag:
		print('What would you like to do today? \n \
			1. Enter Expense Entry \n \
			2. Filter Expenses \n \
			3. Visualize Expenses \n')
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
		else:
			print('Invalid Input!! Please enter a valid integer for the task') 
