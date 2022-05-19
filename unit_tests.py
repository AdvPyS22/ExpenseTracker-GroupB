import unittest

from helper import *
from visualize import Visualize

class UnitTests(unittest.TestCase):
	'''
	Class to host testing functions 
	for all Expense Tracker classes
	and methods. Examples include :
	1. Validation Helper Functions
	2.
	3.
	'''

	def test_helpers(self):
		# Validate Month Function tests
		self.assertTrue(validate_month('01-2021'))
		self.assertTrue(validate_month('04-1999'))
		self.assertFalse(validate_month('13-2022'))
		self.assertFalse(validate_month('-1-2000'))
		self.assertFalse(validate_month('001-2000'))

		# Validate Amount tests
		self.assertTrue(validate_amount(0.125)[0])
		self.assertFalse(validate_amount(0.0)[0])
		self.assertFalse(validate_amount(-22)[0])
		self.assertFalse(validate_amount('Forty Five')[0])

		# Validate Category tests
		self.assertTrue(validate_category('1'))
		self.assertTrue(validate_category('6'))
		self.assertFalse(validate_category('-1'))
		self.assertFalse(validate_category('0'))
		self.assertFalse(validate_category('7'))
		self.assertFalse(validate_category('1.1'))
		
		# Validate Column test
		self.assertTrue(validate_column_names(pd.read_csv('./Expense_no_mistakes.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_column_names(pd.read_csv('./Expense_no_columns.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_column_names(pd.read_csv('./Expense_no_title.csv', header=0, encoding='UTF8')))		
		self.assertFalse(validate_column_names(pd.read_csv('./Expense_no_category.csv', header=0, encoding='UTF8')))		
		self.assertFalse(validate_column_names(pd.read_csv('./Expense_no_date.csv', header=0, encoding='UTF8')))		
		self.assertFalse(validate_column_names(pd.read_csv('./Expense_no_amount.csv', header=0, encoding='UTF8')))		

		# Validate Row test
		self.assertTrue(validate_row_data(pd.read_csv('./Expense_no_mistakes.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_row_data(pd.read_csv('./Expense_2_wrong_category.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_row_data(pd.read_csv('./Expense_2_wrong_date.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_row_data(pd.read_csv('./Expense_2_wrong_Amount.csv', header=0, encoding='UTF8')))
		self.assertFalse(validate_row_data(pd.read_csv('./Expense_2_wrong_all_columns.csv', header=0, encoding='UTF8')))


if __name__ == '__main__':
	print('Performing Unit Tests...')
	unittest.main()