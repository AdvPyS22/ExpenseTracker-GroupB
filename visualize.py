'''
Visualization Class for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''

import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from retrieval import Retrieval
from helper import *

class Visualize:
	'''
	Class to encapsulate all functions
	related to visualization,
	bar charts and pie charts, including
	filtering data functions

	Input
	------------------------------------
	df : Dataframe containing expense entries
	'''
	def __init__(self, df):
		self.df = df
		self.start_visualize_prompt()

	def start_visualize_prompt(self):
		'''
		Handler function to 
		navigate visualization options
		Presents the user with the following options:
			1. Barchart
			2. Piechart
		'''
		input_vis_expense_flag = False
		while not input_vis_expense_flag:
			input_vis_expense = input('Please enter how you would like to visualize the expenses, \n \
					Options are : \n \
					1. Barchart \n \
					2. Piechart \n \
					Enter Option: ')
				
			# Input sanitisation
			try:
				input_vis_expense = int(input_vis_expense)
			except:
				print('Invalid Input!! Please enter a valid integer for the task')
				continue

			# Input Handling
			if input_vis_expense == 1:
				self.vis_barcharts()
				input_vis_expense_flag = True
			elif input_vis_expense == 2:
				self.vis_piecharts()
				input_vis_expense_flag = True
			else:
				print('Please enter a valid visualization task')
		return 0


	def ask_date(self, date_question_str):
	    '''
	    Parameters
	    ----------
	    date_question_str : str
	        The question for the date you want to ask the user. The date has to be in DD-MM-YYYY Format.

	    Returns
	    -------
	    some_date : str
	        The date the user did input in the DD-MM-YYYY Format.
	    '''
	    # Date input and error handling
	    valid_date_flag = False
	    while(not valid_date_flag):
	        some_date = input(date_question_str)
	        valid_date_flag = validate_date(some_date)
	        if not valid_date_flag:
	            print('Please enter a valid date in DD-MM-YYYY Format')
	    return some_date  


	def add_week_month_num(self):
	    '''
	    Parameters
	    ----------
	    df : panda dataframe
	        with following columns:
	            'Date' with datetime type elements
	            
	    Returns
	    -------
	    expense_df : panda dataframe
	        with following columns added:
	            'Weeks' with int type elements
	            'Months' with int type elements
	    '''
	    # Copy dataframe so things can be changed without messing up main dataframe
	    expense_df = self.df.copy(deep = True)
	    # Add columns for number of weeks and months
	    expense_df['Weeks'] = np.zeros(len(expense_df), dtype = int)
	    expense_df['Months'] = np.zeros(len(expense_df), dtype = int)
	    # Fill columns with the number of days and months
	    for rows in range(len(expense_df)):
	        expense_df['Weeks'][rows] = ((expense_df['Date'][rows] - datetime.datetime(1900, 1, 1)) / 7).days
	        expense_df['Months'][rows] = expense_df['Date'][rows].year * 12 + expense_df['Date'][rows].month
	    # Make that the earliest date is week 0
	    expense_df['Weeks'] = expense_df['Weeks'] - np.min(expense_df['Weeks'])
	    expense_df['Months'] = expense_df['Months'] - np.min(expense_df['Months'])
	    return expense_df


	def vis_barcharts(self):
	    '''
	    Parameters
	    ----------
	    df : panda dataframe
	        with following columns:
	            'Amount' with str type elements that can be converted to a float
	            'Date' with datetime type elements

	    Visualizes as a Barplot the expenses from a start date to a end date.
	    The timestep can either be 'Months' or 'Weeks' and are chosen by the user
	    '''    
        # Ask user about the timspan and the time steps he wants to have visualized
	    show_plot = input('What do you want to have visualised. \n \
	                          To display barplot of weekly expense input week or w. \n \
	                          To display barplot of monthly expenses input month or m. \n \
	                          To display both input both or b. \n \
	                          To not diplay anything input anything else. \n \
	                          Enter option:')
	    show_week = show_plot.lower() == 'week' or show_plot.lower() == 'w' or show_plot.lower() == 'both' or show_plot.lower() == 'b'
	    show_month = show_plot.lower() == 'month' or show_plot.lower() == 'm' or show_plot.lower() == 'both' or show_plot.lower() == 'b'
	    # Check if user wanted visualization
	    if show_week or show_month:
	        # Add number of months and weeks to dataframe
	        expense_df = self.add_week_month_num()
	        # Ask for start and end date
	        start_date = self.ask_date('Enter the start Date of the Expenses you want to have visualized as DD-MM-YYYY: ')
	        end_date = self.ask_date('Enter the end Date of the Expenses you want to have visualized as DD-MM-YYYY: ')
	        # Make mask with start and end time
	        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
	        end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
	        date_mask = (expense_df['Date'] >= start_date) & (expense_df['Date'] <= end_date)
	        expense_df = expense_df[date_mask]
	        # Add up all expenses of the same week and plot it
	        if show_week:
	            self.generate_barplot(expense_df, 'Weeks', end_date)
	        # Add up all expenses of the same month and plot it
	        if show_month:
	            self.generate_barplot(expense_df, 'Months', end_date)

	def x_ticks(self, expense_df, time_step, end_date):
	    '''
	    Parameters
	    ----------
	    df : panda datafram
	        with following columns:
	            'Date' with datetime type elements
	            'Weeks' with int type elements
	            'Months' with int type elements   
	    time_step : string
	        time_step is a string either 'Months' or 'Weeks'.
	    end_date : datetime
	        end_date is a chosen date the data point with later dates should not be displayed.

	    Returns
	    -------
	    x_tick_values : list
	        list with the dates of every datapoint in the chosen timestep.
	    '''
	    x_tick_df = expense_df.sort_values('Date', ascending = True)
	    x_tick_df = x_tick_df.drop_duplicates(subset = time_step, keep = 'first')
	    x_tick_values = list(x_tick_df['Date'])
	    for dates in range(len(x_tick_df['Date'])):
	        x_tick_values[dates] = x_tick_values[dates].date()
	    return x_tick_values


	def generate_barplot(self, expense_df, column_str, end_date):
	    '''
	    Parameters
	    ----------
	    expense_df : TYPE
	        With the following columns:
	            'Amount' with str type elements that can be converted to a float
	            'Date' with datetime type elements
	            an column with int type elements you can plot 'Amount' to preferably 'Weeks' or 'Months'
	    column_str : str
	        Describes the column name you want to barplot 'Amount' to.
	    end_date : datetime
	        The date the latest datapoint can be from.

	    Prints
	    -------
	    Barplots with the amount spent either in 'Months' or 'Weeks', 
	    while displaying the first transaction of the timestep.
	    '''
	    diff_weeks = list(set(expense_df[column_str]))
	    expense_per_week = np.zeros(len(diff_weeks), dtype = float)
	    for week in range(len(diff_weeks)):
	        amount_per_week = 0
	        tranactions_per_week = expense_df[expense_df[column_str] == diff_weeks[week]]
	        tranactions_per_week = list(tranactions_per_week['Amount'])
	        for transaction in range(len(tranactions_per_week)):
	            amount_per_week += float(tranactions_per_week[transaction])
	        expense_per_week[week] = amount_per_week
	    diff_weeks = np.asarray(diff_weeks) + 1
	    plt.rcParams.update({'font.size': 13})
	    plt.bar(diff_weeks, expense_per_week, width=1.0)
	    plt.xticks(diff_weeks, self.x_ticks(expense_df, column_str, end_date))
	    plt.xticks(rotation=90)
	    plt.title(column_str[:-1] + 'ly expenses')
	    plt.xlabel(column_str[:-1] + ' within chosen dates')
	    plt.ylabel('Amount of expense')
	    plt.show()


	def vis_piecharts(self):
		'''
		Inputs the type of chart 
		user wishes to visualize
		Options:
		1. Yearly expenses 
		2. Monthly expenses
		3. Expenses in a certain period
		4. Expenses in a certain category 
		Generates the Piechart accordingly
		'''
		input_piechart_flag = False
		while not input_piechart_flag:
			input_piechart_option = input('What do you want to have visualised. \n \
				Options are : \n \
				1. Yearly expenses by category\n \
				2. Monthly expenses by category\n \
				3. Expenses in a certain period by category\n \
				4. Monthly expenses in a certain category in a year\n \
				Enter Option: ')

			# Input sanitisation
			try:
				input_piechart_option = int(input_piechart_option)
			except:
				print('Invalid Input!! Please enter a valid integer for the task')
				continue

			# yearly
			if input_piechart_option == 1:
				input_piechart_flag = self.pie_filter_year()
			# monthly
			elif input_piechart_option == 2:
				input_piechart_flag = self.pie_filter_month()
			# timeframe
			elif input_piechart_option == 3:
				input_piechart_flag = self.pie_filter_timeframe()	
			# category
			elif input_piechart_option == 4:
				# Category input and error handling
				input_piechart_flag = self.pie_filter_category()	
			else :
				print('Please enter a valid pie chart plot task')
		return 0

	def pie_filter_year(self):
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
				print('Please enter a valid year in YYYY Format')
			else:
				datetime_year = datetime.datetime.strptime(year, '%Y')
				df_filter = Retrieval.filter_expenses_by_year(self.df, datetime_year)
				df_filter = df_filter.groupby('Category').sum().reset_index()
				self.pie_yearly(df_filter, year)
		return True

	def pie_filter_month(self):
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
				print('Please enter a valid year in MM-YYYY Format')
			else:
				datetime_month = datetime.datetime.strptime(month, '%m-%Y')
				df_filter = Retrieval.filter_expenses_by_month(self.df, datetime_month)
				df_filter = df_filter.groupby('Category').sum().reset_index()
				self.pie_monthly(df_filter, month)
		return True

	def pie_filter_timeframe(self):
		'''
		Filters dataframe according to a timeframe asked from the user
		
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
				datetime_start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
				datetime_end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
				df_filter = Retrieval.filter_expenses_by_timeframe(self.df, datetime_start_date, \
				                        datetime_end_date)
				df_filter = df_filter.groupby('Category').sum().reset_index()
				self.pie_timeframe(df_filter, start_date, end_date)
		return True

	def pie_filter_category(self):
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
		valid_category_flag = False
		while(not valid_category_flag):
			category = input_category()
			valid_category_flag = validate_category(category)
			if not valid_category_flag:
				print('Please enter a valid category between 1 and 6')
			else:
				valid_year_flag = False
				while not valid_year_flag:
					year = input('Enter the Year as YYYY: ')
					valid_year_flag = validate_year(year)
					if not valid_year_flag:
						print('Please enter a valid year in YYYY Format')
					else:	
						category = int(category)
						df_filter = Retrieval.filter_expenses_by_category(self.df, category)
						df_filter.drop('Category', inplace=True, axis=1)
						df_filter['Month'] =  df_filter['Date'].dt.month
						df_filter = df_filter.groupby('Month').sum().reset_index()
						self.pie_category(df_filter, category, year)
		return True

	def pie_yearly(self, df_filter, year):
		'''
		Parameters
		----------
		df_filter : pandadataframe
			Filtered for the user defined category and year.
		year : str
			Str corresponding to the chosen year.

    	shows pieplot of the share of the categories from the chosen year.
		'''
		labels = []
		items = []
		# fetch category and amount
		for _, row in df_filter.iterrows():
			labels.append(category_dict[row.Category])
			items.append(row.Amount)
		# plot
		plt.pie(items, #autopct='%1.1f%%',
		shadow=False, startangle=90, wedgeprops={"edgecolor": "black"})
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		plt.title(year + " Yearly Category Breakdown", y = 1.05)
		total = sum(items)
		plt.legend(
		labels = ['%s, %1.1f %%' % (l, (float(s) / total) * 100) for l, s in zip(labels, items)],
		loc = "upper left",
		bbox_to_anchor = (0.75,1),
		)
		plt.show() 


	def pie_monthly(self, df_filter, month):
		'''
		Parameters
		----------
		df_filter : pandadataframe
			Filtered for the user defined category and year.
		month : str
			Str corresponding to the chosen month.

    	shows pieplot of the share of the categories from the chosen month.
		'''
		labels = []
		items = []
		# fetch category and amount
		for _, row in df_filter.iterrows():
			labels.append(category_dict[row.Category])
			items.append(row.Amount)
		# plot
		plt.pie(items, #autopct='%1.1f%%',
		shadow=False, startangle=90, wedgeprops={"edgecolor": "black"})
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		plt.title(month + " Monthly Category Breakdown", y = 1.05)
		total = sum(items)
		plt.legend(
		labels = ['%s, %1.1f %%' % (l, (float(s) / total) * 100) for l, s in zip(labels, items)],
		loc = "upper left",
		bbox_to_anchor = (0.75,1),
		)
		plt.show() 


	def pie_timeframe(self, df_filter, start_date, end_date):
		'''
		Parameters
		----------
		df_filter : pandadataframe
			Filtered for the user defined category and year.
		start_date : str
			Str corresponding to the chosen start date.
		year : str
			Str corresponding to the chosen end date.
	
	    shows pieplot of a categories from the chosen timeframe, shares are the months
		'''
		labels = []
		items = []
		# fetch category and amount
		for index, row in df_filter.iterrows():
			labels.append(category_dict[row.Category])
			items.append(row.Amount)
		# plot
		plt.pie(items, #autopct='%1.1f%%',
		    shadow=False, startangle=90, wedgeprops={"edgecolor": "black"})
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		plt.title("From " + start_date + " to " + end_date + " Category Breakdown", y = 1.05)
		total = sum(items)
		plt.legend(
		  labels = ['%s, %1.1f %%' % (l, (float(s) / total) * 100) for l, s in zip(labels, items)],
		  loc = "upper left",
		  bbox_to_anchor = (0.75,1),
		)
		plt.show()   


	def pie_category(self, df_filter, category, year):
		'''
		Parameters
		----------
		df_filter : pandadataframe
			Filtered for the user defined category and year.
		category : int
			Int corresponding to the chosen category.
		year : str
			Str corresponding to the chosen year.

		Returns
		-------
		int
			placeholder.
	
    	shows pieplot of the chosen category in a year and the share of the months
		'''
		labels = []
		items = []
		month_list = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"June",
						8:"August", 9:"Sepetember", 10:"October", 11:"November", 12:"December"}

		# fetch month and amount
		for _, row in df_filter.iterrows():
			labels.append(month_list[row.Month])
			items.append(row.Amount)
		# plot
		plt.pie(items, #autopct='%1.1f%%',
		shadow=False, startangle=90, wedgeprops={"edgecolor": "black"})
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		plt.title("Monthly expenses in "+category_dict[category]+ " in " + year, y = 1.05)
		total = sum(items)
		plt.legend(
		labels = ['%s, %1.1f %%' % (l, (float(s) / total) * 100) for l, s in zip(labels, items)],
		loc = "upper left",
		bbox_to_anchor = (0.75,1),
		)
		plt.show()
		return 0