import datetime

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


def validate_date(string):
	''' 
	Given an input string, validate whether
	it is a valid DD-MM-YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.datetime.strptime(string, '%d-%m-%Y'))
	except ValueError:
		return False


def validate_month(string):
	''' 
	Given an input string, validate whether
	it is a valid MM-YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.datetime.strptime(string, '%m-%Y'))
	except ValueError:
		return False

def validate_year(string):
	''' 
	Given an input string, validate whether
	it is a valid YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.datetime.strptime(string, '%Y'))
	except ValueError:
		return False


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