'''
Retrieval Class for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''

import csv
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helper import *

class Retrieval:
	'''
	Class to retrieve historical data of users' expenses by filters such as by date, month
	year, time window (Start/End Date) or category.
	
	Input
	------------------------------------
	df : Dataframe containing expense entries
	'''
	def __init__(self, df):
		self.df = df
		self.start_retrieval_prompt()

	def start_retrieval_prompt(self):
		'''
		Handler function to 
		navigate filter options
		Presents the user with the following options:
			1. By Date
			2. By Month
			3. By Year
			4. By a window (Start/End Date)
			5. By Category
		'''
		input_filter_expense_flag = False
		while not input_filter_expense_flag:
			input_filter_expense = input('Please enter how you would like to filter the expenses, \n \
				Options are : \n \
				1. By Date \n \
				2. By Month \n \
				3. By Year \n \
				4. By a window (Start/End Date) \n \
				5. By Category \n \
				Enter Option: ')
			
			# Input sanitisation
			try:
				input_filter_expense = int(input_filter_expense)
			except:
				print('Invalid Input!! Please enter a valid integer for the task')
				continue

			# Code block for filtering expenses by a Date
			if input_filter_expense == 1:
				input_filter_expense_flag = self.filter_block_date(self)
			# Code block for filtering expenses by month
			elif input_filter_expense == 2:
				input_filter_expense_flag = self.filter_block_month(self)
			# Code block for filtering expenses by year
			elif input_filter_expense == 3:
				input_filter_expense_flag = self.filter_block_year(self)
			# Code block for filtering expenses by window
			elif input_filter_expense == 4:
				input_filter_expense_flag = self.filter_block_window(self)
			# Code block for filtering expenses by Category
			elif input_filter_expense == 5:
				input_filter_expense_flag = self.filter_block_category(self)
			else :
				print('Please enter a valid filter task')
		return 0

	@staticmethod
	def filter_block_date(self):
		'''
		Filters dataframe according to a date asked from the user
    	
		Parameters
		----------
		df : panda dataframe
			with the column Date containing datetime elements.
	
		Returns
		-------
		bool
			to terminate while loop the function is in.
		'''
		valid_date_flag = False
		while not valid_date_flag:
			date = input('Enter the Date as DD-MM-YYYY: ')
			valid_date_flag = validate_date(date)
			if not valid_date_flag:
				print('Please enter a valid date in DD-MM-YYYY Format')
			else:
				datetime_date = dt.strptime(date, '%d-%m-%Y')
				df_filter = self.filter_expenses_by_date(self.df, datetime_date)
				print(f'Expenses on %s are: ' % datetime_date.strftime('%d %b, %Y'))
				print(df_filter)
		return True
        
	@staticmethod
	def filter_block_month(self):
		'''
		Filters dataframe according to a month asked from the user
	
		Parameters
		----------
		df : panda dataframe
			with the column Date containing datetime elements.

		Returns
		-------
		bool
			to terminate while loop the function is in.
		'''
		valid_month_flag = False
		while not valid_month_flag:
			month = input('Enter the Month as MM-YYYY: ')
			valid_month_flag = validate_month(month)
			if not valid_month_flag:
				print('Please enter a valid month in MM-YYYY Format')
			else:
				datetime_month = dt.strptime(month, '%m-%Y')
				df_filter = self.filter_expenses_by_month(self.df, datetime_month)
				print(f'Expenses on %s are: ' % datetime_month.strftime('%b, %Y'))
				print(df_filter)
		return True
        
	@staticmethod
	def filter_block_year(self):
		'''
		Filters dataframe according to a year asked from the user
	
		Parameters
		----------
		df : panda dataframe
			with the column Date containing datetime elements.

		Returns
		-------
		bool
			to terminate while loop the function is in.
		'''
		valid_year_flag = False
		while not valid_year_flag:
			year = input('Enter the Year as YYYY: ')
			valid_year_flag = validate_year(year)
			if not valid_year_flag:
				print('Please enter a valid month in YYYY Format')
			else:
				datetime_year = dt.strptime(year, '%Y')
				df_filter = self.filter_expenses_by_year(self.df, datetime_year)
				print(f'Expenses on %s are: ' % datetime_year.strftime('%Y'))
				print(df_filter)
		return True


	@staticmethod
	def filter_block_window(self):
		'''
		Filters dataframe according to a time window asked from the user
	
		Parameters
		----------
		df : panda dataframe
			with the column Date containing datetime elements.

		Returns
		-------
		bool
			to terminate while loop the function is in.
		'''
		valid_date_flag = False
		while not valid_date_flag:
			start_date = input('Enter the Start Date as DD-MM-YYYY: ')
			end_date = input('Enter the End Date as DD-MM-YYYY: ')
			valid_date_flag = validate_date(start_date) & validate_date(end_date)
			if not valid_date_flag:
				print('Please enter a valid date in DD-MM-YYYY Format')
			else:
				datetime_start_date = dt.strptime(start_date, '%d-%m-%Y')
				datetime_end_date = dt.strptime(end_date, '%d-%m-%Y')
				df_filter = self.filter_expenses_by_timeframe(self.df, datetime_start_date, \
																datetime_end_date)
				print(f'Expenses within %s and %s are: ' % (datetime_start_date.strftime('%d %b, %Y'),
															datetime_end_date.strftime('%d %b, %Y'))
					)
				print(df_filter)
		return True

	@staticmethod
	def filter_block_category(self):
		'''
		Filters dataframe according to a category asked from the user
		
		Parameters
		----------
		df : panda dataframe
			with the column Date containing datetime elements.
	
		Returns
		-------
		bool
			to terminate while loop the function is in.
		'''
		valid_category_flag = False
		while(not valid_category_flag):
			category = input_category()
			valid_category_flag = validate_category(category)
			if not valid_category_flag:
				print('Please enter a valid category between 1 and 6')
			else:
				category = int(category)
				df_filter = self.filter_expenses_by_category(self.df, category)
				print(f'Expenses with Category %d are: ' % category)
				print(df_filter)
		return True

	@staticmethod
	def filter_expenses_by_date(df, date):
		'''
		Filter entries by input date
		and return the filtered Dateframe
		'''
		return df[df['Date'] == date.strftime('%Y-%m-%d')]

	@staticmethod
	def filter_expenses_by_month(df, datetime_month):
		'''
		Filter entries by input month
		and return the filtered Dateframe
		'''
		first_day = datetime_month.strftime("%Y-%m-01")
		n_days = days_in_month(datetime_month.strftime('%m'), datetime_month.strftime('%Y'))
		last_day = datetime_month.strftime("%Y-%m-" + str(n_days))
		return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]

	@staticmethod
	def filter_expenses_by_year(df, datetime_year):
		'''
		Filter entries by input year
		and return the filtered Dateframe
		'''
		first_day = datetime_year.strftime("%Y-01-01")
		last_day = datetime_year.strftime("%Y-12-31") 
		return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]

	@staticmethod
	def filter_expenses_by_timeframe(df, start_date, end_date):
		'''
		Filter entries by input
		start and end date
		Returns the filtered Dataframe
		'''
		start_date_f = start_date.strftime('%Y-%m-%d')
		end_date_f = end_date.strftime('%Y-%m-%d')
		return 	df[(df['Date'] >= start_date_f) & (df['Date'] <= end_date_f)]

	@staticmethod
	def filter_expenses_by_category(df, category):
		'''
		Filter entries by 
		Category and return the 
		filtered Dataframe 
		'''
		return df[df['Category'] == category]


