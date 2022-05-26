# ExpenseTracker-GroupB

Advanced Python - Spring 2022 Project

An app where the user can manage all their expenses in one place. Adding, Editing or Visualizing made simple 

To activate the virtual-environment setup, including the set of dependencies with their required version libraries, use the following command prior to running the modules :

`source venvironment/bin/activate`

# Roadmap
## April 28th
- Building Roadmap
- Implement functionality for user to add their expenses, specifying the following fields :
	- Title
	- Category 
	- Date 
	- Amount 
- Saving each edit to a csv

Category can be one of the following : *Groceries, Entertainment, Travel, Shopping, Bills, Leasure* or *Investments*

### Execution

- Run `python main.py` or `python3 main.py` in terminal.
- Example case:

  ```bash
  (base) kitamado:project-Deliverable-1 a0$ python main.py
  Welcome to Expense Tracker!
  Let's start adding Expenses
  Enter the Title of the Expense: wii
  Enter Category as an Integer as follows: 
    1 : Groceries 
    2 : Entertainment 
    3 : Travel 
    4 : Shopping 
    5 : Bills 
    6 : Investments 
    Category: 2
  Enter the Date of the Expense as DD-MM-YYYY: 25-03-2021
  Enter the Amount: 39.7
  Expense successfully saved!
  ```


## May 5th
- Implement functionality for user to retrieve their expense data by date, timeframe or categories
	- Load data from a csv file
	- Allow filtering data by Date
	- Allow filtering data by a window (timeframe)
	- Allow filtering data by categoeis
- Implement Visualizations for expenses by week, month and categories
	- Barchart or Piechart of weekly expenses
	- Barchart or Piechart of monthly expenses
	- Piechart of overall expenses by category
- Creating GitHub repository and commit all previous code

## May 12th
- Code refactoring - Pylint feedback
- Code refactoring - Object Oriented Programming
	- Implement Expense Visualization Class

## May 19th
- Refactor code to use Try-Catch blocks for handling Exceptions
	- For handling poorly formatted input (For ex. Date)
- Implement Unit Tests with atleast 4 test cases

Run `python3 unit_tests.py -v` in terminal.

## June 2nd
- Set up virtual environment for all code dependencies and running the project
- Implement Functionality that allows user to select and edit expense entries 
	- User can filter expenses and select entries using Expense-ID identifier
	- Editing each entry can be done field by field 
- Prepare README.md
	- Exemplify with illustrations various functionalities of the module
