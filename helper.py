import datetime

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