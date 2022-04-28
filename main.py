'''
Main File for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''
import csv
from datetime import datetime

def save_expense_entry(title, category, date, amount, csv_file):
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
		with open(csv_file, 'a') as f:
		    writer = csv.writer(f)
		    writer.writerow(entry_list)
		return True 
	except:
		return False


def validate_date(string):
	''' 
	Given an input string, validate whether
	it is a valid DD-MM-YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.strptime(string, '%d-%m-%Y'))
	except ValueError:
		return False
	

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def validate_amount(string):
	''' 
	Validation of input as a valid float
	'''
	try:
		amount = float(string)
		return (amount > 0), amount
	except:
		return False, -1


def validate_category(string):
	'''
	Given input string, validate 
	whether it is an integer between 1 and 6
	'''
	try:
		category = int(string)
		if category>0 and category<=6:
			return True
	except:
		pass
	return False


def input_category():
	# Category input string 
	return input('Enter Category as an Integer as follows: \n \
	1 : Groceries \n \
	2 : Entertainment \n \
	3 : Travel \n \
	4 : Shopping \n \
	5 : Bills \n \
	6 : Investments \n \
	Category: ')


if __name__ == '__main__':
	print('Welcome to Expense Tracker!')
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

	data_file = './Expense.csv'
	if save_expense_entry(title, category, date, amount, data_file):
		print('Expense successfully saved!')
	else:
		print('Oops! We ran into some trouble. Please try again later')

