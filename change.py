'''
Change Class for Expense Tracker - Group 10
Members : Shunyu Wu, Jerome Staeheli, Kartik Kohli
'''
import csv
import pandas as pd
from helper import *

class Change:
    '''
    Class to find and change a entry.
    
    Input
    ------------------------------------
    df : Dataframe containing expense entries
    '''
    def __init__(self, df):
        self.df = df
        self.start_enrty_change()
        
    def start_enrty_change(self):
        '''
        Takes a dataframe and input from user and changes the entries in the csv file

        Creates
        -------
        New updated csv.
        '''
        input_flag = False
        
        while not input_flag:
            
            # Asks the user if the user can find the entry the user wants to change
            print(self.df)

            user_input = input('Do you see the entry you want to change? [Y/N]: ')
            
            if user_input.lower() == 'yes' or user_input.lower() == 'y':
                self.change_entry()
                input_flag = True

            elif user_input.lower() == 'no' or user_input.lower() == 'n':
                self.no_filter_path()
                input_flag = True

            else:
                print('You did not chose an existing option.')


    def no_filter_path(self):
        '''
        Asks the user if the user wants to filter for an element in one column
        and asks afterwards if the user has found the value the user wants to change

        If an entry is found the user can change it. 
        If the entry is not found the user is told that it eighter does not exist
        or that the user made a typo
        '''
        
        entry_not_found = True
        
        # Asks the user if the user wants to do a title search
        user_answer = self.yes_no('Do you want to search for a title?')
        if user_answer:
            entry_not_found = self.search('Please input your title (Sensitive to lower and upper case letters): ', 'Title')

        # Asks the user if the user wants to do a category search
        if entry_not_found:
            user_answer = self.yes_no('Do you want to search for a category?')
            if user_answer:
                entry_not_found = self.search('Please input your category (categories goes from 1-6): ', 'Category')

        # Asks the user if the user wants to do a date search
        if entry_not_found:
            user_answer = self.yes_no('Do you want to search for a date?')
            if user_answer:
                entry_not_found = self.search('Please input your date in YYYY-MM-DD format (has to be this format): ', 'Date')

        # Asks the user if the user wants to do a amount search
        if entry_not_found:
            user_answer = self.yes_no('Do you want to search for a amount?')
            if user_answer:
                entry_not_found = self.search('Please input your amount as a number: ', 'Amount')

        # Directs the user to the entry change when the entry is found 
        #otherwise the user is told that it does not exist or that the user made a typo
        if entry_not_found:
            print('Eighter your entry does not exist or you did a typo.')
        else:
            self.change_entry()

    
    def search(self, message_string, column):
        '''
        Parameters
        ----------
        message_string : str
            The question that asks the user to input a value the user thinks is in the column.
        column : str
            The string for the column that needs to be searched.

        Returns
        -------
        bool
            Answer to the question if the user has found the entry the user is looking for.
        '''
        user_value = input(message_string)
        
        # Changes the data type for Category and amount since they are in a diffrent data type
        if column == 'Category':
            user_value = int(user_value)
        elif column == 'Amount':
            user_value = float(user_value)
        
        # Print the filtered dataframe and ask the user if the user can find the entry the user wants to change
        print(self.df[self.df[column] == user_value])
        user_answer = self.yes_no('Did you find your entry?')
        
        # Swap around true and false so if statements do not need not
        return not user_answer
        
    
    def yes_no(self, message_string):
        '''
        Parameters
        ----------
        message_string : str
            A string you tell the user.

        Returns
        -------
        bool
            If the answer is yes the method/function returns true.
        '''
        
        # Cases that mean yes
        yes = ('yes', 'y')
        
        # Print custum question
        print()
        print(message_string, end = '')
        
        # User answer and the check for it
        user_yes = input('Type Yes, yes, Y or y if the answer is yes: ')
        if user_yes.lower() in yes:
            return True
        return False
    

    def change_entry(self):
        '''
        Asks the user which row the user wants to change and updates the csv file
        '''
        
        # Ask user which line the user wants to change and check if the row exists
        change_flag = False
        while not change_flag:
            print()
            print('Please type the number in the left of the entry you want to change.', end = '')
            user_change = input('For example, to change the entry  5  Clothes   4  2022-09-01  36.00  you would type 5: ')
            try:
                self.df.iloc[int(user_change)]
                change_flag = True
            except:
                print('You did not choos a number that is available.')
        
        # Ask the user for updated entries, starting with the title
        print('The current title of the entry is:', self.df['Title'][int(user_change)])
        user_title = input('Please provide the new Title:')
        
        # Category input and error handling
        print('The current Category of the entry is:', self.df['Category'][int(user_change)])
        print('Please provide the new Category:')             
        valid_category_flag = False
        while(not valid_category_flag):
            category = input_category()
            valid_category_flag = validate_category(category)
            if not valid_category_flag:
                print('Please enter a valid category between 1 and 6')

        # Date input and error handling
        print('The current Date of the entry is:', self.df['Date'][int(user_change)])
        print('Please provide the new Date as DD-MM-YYYY: ')
        valid_date_flag = False
        while(not valid_date_flag):
            date = input()
            valid_date_flag = validate_date(date)
            if not valid_date_flag:
                print('Please enter a valid date in DD-MM-YYYY Format')

        # Amount input and error handling
        print('The current Amount of the entry is:', self.df['Amount'][int(user_change)])
        print('Please provide the new Amount: ')       
        valid_amount_flag = False
        while(not valid_amount_flag):
            amount = input()
            valid_amount_flag, amount = validate_amount(amount)
            if not valid_amount_flag:
                print('Please enter a valid amount value')
        
        entry_list = [user_title, category, date, str(amount)]

        # Generates list mit changed row
        with open('./Expense.csv', 'r') as f:
            loop_num = 0
            temp_list = []
            for row in f:
                if loop_num == int(user_change) + 1:
                    temp_list.append(entry_list)        
                else:
                    temp_list.append(row.rstrip().split(','))
                loop_num += 1
            temp_list.remove([''])
            print(temp_list)

        # Saves the updated list as the csv file
        with open('./Expense.csv', 'w',  newline = "") as f:
            writer = csv.writer(f)

            writer.writerows(temp_list)
                
        
            
            