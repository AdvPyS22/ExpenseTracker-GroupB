import datetime
import pandas as pd

category_dict = {1:'Groceries', 2:'Entertainment', 3:'Travel', 4:'Shopping', 5:'Bills', 6:'Investments'}

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
		if 0 < category <= 6:
			return True
	except:
		pass
	return False


def validate_column_names(df):
    '''
    Parameters
    ----------
    df : Panda dataframe
        any panda dataframe.

    Returns
    -------
    Returns False if a column is missing.
    '''    
    header_list = ['Title', 'Category', 'Date', 'Amount']

    try:
        import_headers = df.axes[1] #==> 1 is to identify columns
        miss_match_header = [i for i in import_headers if i not in header_list]
        # assert (len(miss_match_header) == 0)
        if len(miss_match_header) == 0:
            raise NameError("The first row of your ./Expense.csv file is not excepted header list.") 

    except:
        print('The first row of your ./Expense.csv file is not excepted header list.')
        print('Check your csv if the first row looks like this: \n \
                  Title,Category,Date,Amount')
        print('or delete csv.')
        return False
    return True
        
    
def validate_row_data(df):
    '''
    Checks if every row in every column has the right format
    
    Parameters
    ----------
    df : Panda Dataframe
        Dataframe with the columns Title, Category, Date and Amount.

    Returns
    -------
    Prints out a error message where the faulty entry can be found.
    Terminates the execution of the code.
    '''
    all_columns = ['Title', 'Category', 'Date', 'Amount']
    
    faulty_date_rows = []
    faulty_category_rows = []
    faulty_amount_rows = []
    
    # Check every row for wrong formats
    for row in range(len(df)):
        if not validate_category(df['Category'][row]):
            faulty_category_rows.append(row + 1) 
        if not validate_date(df['Date'][row]):
            faulty_date_rows.append(row + 1)  
        if not validate_amount(df['Amount'][row])[0]:
            faulty_amount_rows.append(row + 1)
    
    cat_bool    = faulty_category_rows == []
    date_bool   = faulty_date_rows   == []
    amount_bool = faulty_amount_rows == []
    
    # Return which rows contain the entries with the wrong format
    if date_bool == False or cat_bool == False or amount_bool == False:
        wrong_format = ' in the following rows are not in the right format:'
        ask_str = 'Please change the format to:'
        print('Your csv contains entries, that are not in the right format')
            
        if cat_bool == False:
            print('The Category' + wrong_format)
            print(faulty_category_rows)
            print(ask_str)
            print('An whole number from 1 to 6')            

        if date_bool == False:
            print('The Date' + wrong_format)
            print(faulty_date_rows)
            print(ask_str)
            print('DD-MM-YYYY')
            
        if amount_bool == False:
            print('The Amount' + wrong_format)
            print(faulty_amount_rows)
            print(ask_str)
            print('A number that can be converted to a float')           
        
        return False
    return True
        
def days_in_month(month, year):
    '''
    Returns the number of days in the input Month
    '''
    def leap_year(year):
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        if leap_year(year):
            return 29
        return 28
    return 30