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
            
            print(self.df)
            
            
            user_input = input('Do you see the entry you want to change? [Y/N]: ')
            
            if user_input.lower() == 'yes' or user_input.lower() == 'y':
                self.change_entry()
                input_flag = True

            elif user_input.lower() == 'no' or user_input.lower() == 'n':
                print('works no')
                input_flag = True
                
            else:
                print('You did not chose an existing option.')


    def change_entry(self):
        '''
        Asks the user which row the user wants to change and updates the csv file
        '''
        
        # Ask user which line the user wants to change and check if the row exists
        change_flag = False
        while not change_flag:
            user_change = input('Please type the number in front of the entry you want to change: ')
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
                
        
            
            