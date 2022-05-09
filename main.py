'''
Main File for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


DATA_FILE = './Expense.csv'
category_dict = {1:'Groceries', 2:'Entertainment', 3:'Travel', 4:'Shopping', 5:'Bills', 6:'Investments'}

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


def add_week_month_num(df):
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
    expense_df = df.copy(deep = True)
    # Add columns for number of weeks and months
    expense_df['Weeks'] = np.zeros(len(expense_df), dtype = int)
    expense_df['Months'] = np.zeros(len(expense_df), dtype = int)
    # Fill columns with the number of days and months
    for rows in range(len(expense_df)):
        expense_df['Weeks'][rows] = ((expense_df['Date'][rows] - datetime(1900, 1, 1)) / 7).days
        expense_df['Months'][rows] = expense_df['Date'][rows].year * 12 + expense_df['Date'][rows].month
    # Make that the earliest date is week 0
    expense_df['Weeks'] = expense_df['Weeks'] - np.min(expense_df['Weeks'])
    expense_df['Months'] = expense_df['Months'] - np.min(expense_df['Months'])
    return expense_df

def x_ticks(df, time_step, end_date):
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
    x_tick_df = df.sort_values('Date', ascending = True)
    x_tick_df = x_tick_df.drop_duplicates(subset = time_step, keep = 'first')
    x_tick_values = list(x_tick_df['Date'])
    for dates in range(len(x_tick_df['Date'])):
        x_tick_values[dates] = x_tick_values[dates].date()
    return x_tick_values

def vis_barcharts(df):
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
    # Check if user wanted visualization
    if show_plot.lower() != 'week' or show_plot.lower() != 'w' or show_plot.lower() != 'both' or show_plot.lower() != 'b' or show_plot.lower() != 'month' or show_plot.lower() != 'm':
        expense_df = add_week_month_num(df)
        
        # Date input and error handling
        valid_date_flag = False
        while(not valid_date_flag):
            start_date = input('Enter the start Date of the Expensees you want to have visualized as DD-MM-YYYY: ')
            valid_date_flag = validate_date(start_date)
            if not valid_date_flag:
                print('Please enter a valid date in DD-MM-YYYY Format')
        valid_date_flag = False
        while(not valid_date_flag):
            end_date = input('Enter the start Date of the Expensees you want to have visualized as DD-MM-YYYY: ')
            valid_date_flag = validate_date(end_date)
            if not valid_date_flag:
                print('Please enter a valid date in DD-MM-YYYY Format')
        # Make mask with start and end time
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')
        date_mask = (expense_df['Date'] >= start_date) & (expense_df['Date'] <= end_date)
        expense_df = expense_df[date_mask]
        
        # Add up all expenses of the same week and plot it
        if show_plot.lower() == 'week' or show_plot.lower() == 'w' or show_plot.lower() == 'both' or show_plot.lower() == 'b':
            diff_weeks = list(set(expense_df['Weeks']))
            expense_per_week = np.zeros(len(diff_weeks), dtype = float)
            for week in range(len(diff_weeks)):
                amount_per_week = 0
                tranactions_per_week = expense_df[expense_df['Weeks'] == diff_weeks[week]]
                tranactions_per_week = list(tranactions_per_week['Amount'])
                for transaction in range(len(tranactions_per_week)):
                    amount_per_week += float(tranactions_per_week[transaction])
                expense_per_week[week] = amount_per_week
            diff_weeks = np.asarray(diff_weeks) + 1
            plt.rcParams.update({'font.size': 13})
            plt.bar(diff_weeks, expense_per_week, width=1.0)
            plt.xticks(diff_weeks, x_ticks(expense_df, 'Weeks', end_date))
            plt.xticks(rotation=90)
            plt.title('Weekly expenses')
            plt.xlabel('Week within chosen dates')
            plt.ylabel('Amount of expense')
            plt.show()
        # Add up all expenses of the same month and plot it
        if show_plot.lower() == 'month' or show_plot.lower() == 'm' or show_plot.lower() == 'both' or show_plot.lower() == 'b':
            diff_month = list(set(expense_df['Months']))
            expense_per_month = np.zeros(len(diff_month), dtype = float)
            for month in range(len(diff_month)):
                amount_per_month = 0
                tranactions_per_month = expense_df[expense_df['Months'] == diff_month[month]]
                tranactions_per_month = list(tranactions_per_month['Amount'])
                for transaction in range(len(tranactions_per_month)):
                    amount_per_month += float(tranactions_per_month[transaction])
                expense_per_month[month] = amount_per_month
            diff_month = np.asarray(diff_month) + 1
            plt.bar(diff_month, expense_per_month, width=1.0)
            plt.xticks(diff_month, x_ticks(expense_df, 'Months', end_date))
            plt.xticks(rotation=90)
            plt.title('Monthly expenses')
            plt.xlabel('Month within chosen dates')
            plt.ylabel('Amount of expense')
            plt.show()
    return 0

def pie_yearly(df_filter, year):
	'''
	draw yearly pie chart by category
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

def pie_monthly(df_filter, month):
	'''
	draw yearly pie chart by category
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

def pie_timeframe(df_filter, start_date, end_date):
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

def pie_category(df_filter, category, year):
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

def vis_piecharts(df):
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
			valid_year_flag = False
			while not valid_year_flag:
				year = input('Enter the Year as YYYY: ')
				valid_year_flag = validate_year(year)
				if not valid_year_flag:
					print('Please enter a valid year in YYYY Format')
				else:
					datetime_year = datetime.strptime(year, '%Y')
					df_filter = filter_expenses_by_year(df, datetime_year)
					df_filter = df_filter.groupby('Category').sum().reset_index()
					pie_yearly(df_filter, year)
			input_piechart_flag = True

		# monthly
		elif input_piechart_option == 2:
			valid_month_flag = False
			while not valid_month_flag:
				month = input('Enter the Month as MM-YYYY: ')
				valid_month_flag = validate_month(month)
				if not valid_month_flag:
					print('Please enter a valid year in MM-YYYY Format')
				else:
					datetime_month = datetime.strptime(month, '%m-%Y')
					df_filter = filter_expenses_by_month(df, datetime_month)
					df_filter = df_filter.groupby('Category').sum().reset_index()
					pie_monthly(df_filter, month)
			input_piechart_flag = True


		# timeframe
		elif input_piechart_option == 3:
			valid_date_flag = False
			while not valid_date_flag:
				start_date = input('Enter the Start Date as DD-MM-YYYY: ')
				end_date = input('Enter the End Date as DD-MM-YYYY: ')
				valid_date_flag = validate_date(start_date) & validate_date(end_date)
				if not valid_date_flag:
					print('Please enter a valid date in DD-MM-YYYY Format')
				else:
					datetime_start_date = datetime.strptime(start_date, '%d-%m-%Y')
					datetime_end_date = datetime.strptime(end_date, '%d-%m-%Y')
					df_filter = filter_expenses_by_timeframe(df, datetime_start_date, \
					                        datetime_end_date)
					df_filter = df_filter.groupby('Category').sum().reset_index()
					pie_timeframe(df_filter, start_date, end_date)
			input_piechart_flag = True	

		# category
		elif input_piechart_option == 4:
			# Category input and error handling
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
							df_filter = filter_expenses_by_category(df, category)
							df_filter.drop('Category', inplace=True, axis=1)
							df_filter['Month'] =  df_filter['Date'].dt.month
							df_filter = df_filter.groupby('Month').sum().reset_index()
							pie_category(df_filter, category, year)

			input_piechart_flag = True	
		else :
			print('Please enter a valid pie chart plot task')
	return 0



def visualize_expenses(df):
	'''
	Handler function to 
	navigate visualization options
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
			vis_barcharts(df)
			input_vis_expense_flag = True
		elif input_vis_expense == 2:
			vis_piecharts(df)
			input_vis_expense_flag = True
		else:
			print('Please enter a valid visualization task')
	return 0


def filter_expenses(df):
	'''
	Present options to the 
	user on the basis of which
	filter task to perform
	Options:
	1. By Date
	2. By Month
	3. By a window (Start/End Date)
	4. By Category
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
			valid_date_flag = False
			while not valid_date_flag:
				date = input('Enter the Date as DD-MM-YYYY: ')
				valid_date_flag = validate_date(date)
				if not valid_date_flag:
					print('Please enter a valid date in DD-MM-YYYY Format')
				else:
					datetime_date = datetime.strptime(date, '%d-%m-%Y')
					df_filter = filter_expenses_by_date(df, datetime_date)
					print(f'Expenses on %s are: ' % datetime_date.strftime('%d %b, %Y'))
					print(df_filter)
			input_filter_expense_flag = True
		# Code block for filtering expenses by month
		elif input_filter_expense == 2:
			valid_month_flag = False
			while not valid_month_flag:
				month = input('Enter the Month as MM-YYYY: ')
				valid_month_flag = validate_month(month)
				if not valid_month_flag:
					print('Please enter a valid month in MM-YYYY Format')
				else:
					datetime_month = datetime.strptime(month, '%m-%Y')
					df_filter = filter_expenses_by_month(df, datetime_month)
					print(f'Expenses on %s are: ' % datetime_month.strftime('%b, %Y'))
					print(df_filter)
			input_filter_expense_flag = True

		# Code block for filtering expenses by year
		elif input_filter_expense == 3:
			valid_year_flag = False
			while not valid_year_flag:
				year = input('Enter the Year as YYYY: ')
				valid_year_flag = validate_year(year)
				if not valid_year_flag:
					print('Please enter a valid month in YYYY Format')
				else:
					datetime_year = datetime.strptime(year, '%Y')
					df_filter = filter_expenses_by_year(df, datetime_year)
					print(f'Expenses on %s are: ' % datetime_year.strftime('%Y'))
					print(df_filter)
			input_filter_expense_flag = True

		# Code block for filtering expenses by window
		elif input_filter_expense == 4:
			valid_date_flag = False
			while not valid_date_flag:
				start_date = input('Enter the Start Date as DD-MM-YYYY: ')
				end_date = input('Enter the End Date as DD-MM-YYYY: ')
				valid_date_flag = validate_date(start_date) & validate_date(end_date)
				if not valid_date_flag:
					print('Please enter a valid date in DD-MM-YYYY Format')
				else:
					datetime_start_date = datetime.strptime(start_date, '%d-%m-%Y')
					datetime_end_date = datetime.strptime(end_date, '%d-%m-%Y')
					df_filter = filter_expenses_by_timeframe(df, datetime_start_date, \
																	datetime_end_date)
					print(f'Expenses within %s and %s are: ' % (datetime_start_date.strftime('%d %b, %Y'),
																datetime_end_date.strftime('%d %b, %Y'))
						)
					print(df_filter)
			input_filter_expense_flag = True
		# Code block for filtering expenses by Category
		elif input_filter_expense == 5:
			valid_category_flag = False
			while(not valid_category_flag):
				category = input_category()
				valid_category_flag = validate_category(category)
				if not valid_category_flag:
					print('Please enter a valid category between 1 and 6')
				else:
					category = int(category)
					df_filter = filter_expenses_by_category(df, category)
					print(f'Expenses with Category %d are: ' % category)
					print(df_filter)
			input_filter_expense_flag = True
		else :
			print('Please enter a valid filter task')
	return 0


def filter_expenses_by_date(df, date):
	'''
	Filter entries by input date
	and return the filtered Dateframe
	'''
	return df[df['Date'] == date.strftime('%Y-%m-%d')]

def filter_expenses_by_month(df, datetime_month):
	'''
	Filter entries by input month
	and return the filtered Dateframe
	'''
	first_day = datetime_month.strftime("%Y-%m-01")
	last_day = datetime_month.strftime("%Y-%m-31") # it doesn't matter if the month has less than 31 days.
	return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]

def filter_expenses_by_year(df, datetime_year):
	'''
	Filter entries by input year
	and return the filtered Dateframe
	'''
	first_day = datetime_year.strftime("%Y-01-01")
	last_day = datetime_year.strftime("%Y-12-31") 
	return 	df[(df['Date'] >= first_day) & (df['Date'] <= last_day)]


def filter_expenses_by_timeframe(df, start_date, end_date):
	'''
	Filter entries by input
	start and end date
	Returns the filtered Dataframe
	'''
	start_date_f = start_date.strftime('%Y-%m-%d')
	end_date_f = end_date.strftime('%Y-%m-%d')
	return 	df[(df['Date'] >= start_date_f) & (df['Date'] <= end_date_f)]


def filter_expenses_by_category(df, category):
	'''
	Filter entries by 
	Category and return the 
	filtered Dataframe 
	'''
	return df[df['Category'] == category]


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


def validate_month(string):
	''' 
	Given an input string, validate whether
	it is a valid MM-YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.strptime(string, '%m-%Y'))
	except ValueError:
		return False

def validate_year(string):
	''' 
	Given an input string, validate whether
	it is a valid YYYY format 
	Returns True if it is valid, False otherwise
	'''
	try:
		return bool(datetime.strptime(string, '%Y'))
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
			filter_expenses(df)
			input_task_flag = True
		elif input_task == 3:
			visualize_expenses(df)
			input_task_flag = True
		else:
			print('Invalid Input!! Please enter a valid integer for the task') 
