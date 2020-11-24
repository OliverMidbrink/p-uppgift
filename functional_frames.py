#import tkinter for GUI purposes
import tkinter as tk
from tkscrolledframe import ScrolledFrame
from tkinter.ttk import *
from pages import *

# Mostly for web-scraping used in the StockSelector search_stock method
import requests
from bs4 import BeautifulSoup

# For data purposes
import pandas

# Results frame to show specific data, for example fundamental analysis data or technical analysis data or
# even beta ranking list
class Table(tk.Frame):

    # Initialize results frame with data in the form of an array
    def __init__(self, parent, data_frame):
        tk.Frame.__init__(self, parent)

        # Create results frame using the data variable


# Navigation frame with title in right top corner and back to main menu button in top left corner
class NavigationFrame(tk.Frame):

    # Initalize navigation frame with page title and navigation command as input. Also parent which is where
    # the navigation frame is located
    def __init__(self, parent, page_title, navigation_command):
        tk.Frame.__init__(self, parent)

        # Back to menu button
        back_button = tk.Button(self, text="Back to Main Menu",
                                command=navigation_command)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Page title
        title = tk.Label(self, text=page_title, font=("Times", 16, "bold"))
        title.grid(row=0, column=1, padx=10, pady=10, sticky='w')


# StockSelector is a frame that lets the user choose a stock from internet search
class StockSelectorFrame(tk.Frame):

    # Initialize StockSelector
    def __init__(self, parent, function_to_run, controller, should_hide_when_selected):

        # Set what function should be run with the selected stock
        # for example fundamental or technical analysis
        self.function_to_run = function_to_run

        # Save controller class as attribute
        self.controller = controller

        # Save should_hide_when_selected as attribute
        self.should_hide_when_selected = should_hide_when_selected

        # Initialize parent class
        tk.Frame.__init__(self, parent)

        # Descriptive label for search bar
        search_label = tk.Label(self, text="Search stock by company name or symbol: ")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # Search function for searching up stocks. Used both in search button and entry
        def search_function(*args):
            self.display_search_results(self.search_stock(search_bar.get()))

        # Search field for stock keyword
        search_bar = tk.Entry(self)
        search_bar.grid(row=0, column=1, padx=10, pady=10)

        # Save search_bar as attribute
        self.search_bar = search_bar

        # Bind search_bar enter to searching stocks
        search_bar.bind("<Return>", search_function)

        # Search button that when pressed, feeds the
        # string from search_bar to search_stock method as well as
        # should_hide_when_selected.
        search_button = tk.Button(self, text="Search", command=search_function)
        search_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    def log_financial_item_info(self, financial_item_info):
        # Output information of financial item to terminal/console
        print('Result __________')
        print('Symbol: ', financial_item_info['symbol'])
        print('Name: ', financial_item_info['name'])
        print('Last price: ', financial_item_info['last_price'])
        print('Industry/category: ', financial_item_info['industry_or_category'])
        print('Type: ', financial_item_info['type'])
        print('Exchange: ', financial_item_info['exchange'])

    def search_stock(self, keywords):
        # Search for the stocks and create a list with search results
        print('Searched for: ', keywords)

        # Escape keywords to fit better in url
        #escaped_keywords = re.escape(keywords)

        # Create search url
        URL = "https://finance.yahoo.com/lookup?s=" + keywords
        print(URL)

        # Use requests to download information including html
        results_page = requests.get(URL)

        # Create a BeautifulSoup object using the html from the
        # results page for web-scraping and extracting the relevant results
        soup = BeautifulSoup(results_page.content, 'html.parser')

        # Get all search results, including not only stocks but also ETF
        # and MUTUAL FUND. The first row is column information so do not
        # include it (Hence "[1:]"). Tr is a tag used for marking rows
        # in yahoo finance
        all_html_results = soup.find_all('tr')[1:]


        # Create temporary list to store all the stock search results
        stock_result_list = []

        # Iterate through search results and create info dictionaries for each
        # result. Then filter only for stocks by adding only stocks to stock_results
        for result in all_html_results:

            # List for storing information for this current result
            # (that will be of type STOCK or ETF or MUTUAL FUND or other)
            result_info = [0] * 6

            # Get all the html columns of this result
            columns = result.find_all('td')

            # Get the symbol name of result, strip() to remove leading and trailing spaces
            result_info[0] = columns[0].find('a').get_text().strip()

            # Get the name of result
            result_info[1] = columns[1].get_text()

            # Get the Last price of result
            result_info[2] = columns[2].get_text()

            # Get the industry of the result
            result_info[3] = columns[3].get_text()

            # Get the type of the result (for example stock or etf)
            result_info[4] = columns[4].get_text()

            # Get the Exchange that trades this result
            result_info[5] = columns[5].get_text()

            # Log information about this financial item result
            # self.log_financial_item_info(result_info)

            # If the search result is a stock, add its data to stock_results
            if 'Stocks' in result_info[4]:
                # Append all stock search results to temporary stock result list
                stock_result_list.append(result_info)

        # Column names for search results data
        col_names = ['Symbol', 'Name', 'Last Price', 'Industry/Category', 'Type', 'Exchange']

        # List for storing stock results from search
        search_results_data_frame = pandas.DataFrame(stock_result_list, columns=col_names)

        print('Data frame: \n', search_results_data_frame)
        return search_results_data_frame

    # Function that displays the search results from the user input in the form ao
    def display_search_results(self, stock_results_dataframe):
        # stock_results is a list containing dictionaries. Each dictionary represents a stock
        # . The stock dictionaries contain keywords 'symbol', 'name', 'last_price', 'industry_or_category'
        # as well as 'type', 'exchange'

        # Display the search results and let user select stock

        # Scrolled frame for results
        sf_stock_results = ScrolledFrame(self, width=810, height=500)
        sf_stock_results.grid(row=1, column=0, columnspan=3)

        # Save sf_stock_results as attribute
        self.sf_stock_results = sf_stock_results

        # Bind arrow keys and scroll wheel for scrolling functionality
        sf_stock_results.bind_scroll_wheel(self.controller)
        sf_stock_results.bind_arrow_keys(self.controller)

        # Inner frame that is displayed inside the scrollable frame
        inner_frame = sf_stock_results.display_widget(tk.Frame)

        # Set the column names if there are any search results
        if len(stock_results_dataframe) > 0:
            # set column names
            col_names = stock_results_dataframe.columns
            # Iterate through column names
            for col_idx in range(len(stock_results_dataframe.columns)):
                col_label = tk.Label(inner_frame, text=col_names[col_idx], font=('Arial', 15, 'bold'))
                col_label.grid(row=0, column=col_idx, sticky='w')
        # Otherwise tell user there were no results
        else:
            no_results_label = tk.Label(inner_frame, text='No search reults for keyword: ' + self.search_bar.get())
            no_results_label.grid(row=0, column=0, sticky='w')

        # Here are the column keys
        col_keys = stock_results_dataframe.columns

        # Iterate through rows and columns and add all data for resulting stocks
        for row_idx in range(len(stock_results_dataframe.index)):

            # Separate rows for easier navigation using separator class
            Separator(inner_frame, orient='horizontal').grid(row=row_idx * 2 + 1,
                                                             column=0,
                                                             sticky='ew',
                                                             columnspan=7
                                                             )
            # Create select stock button for each row

            # Function that runs this stock_selectors function_to_run with
            # the selected stock.
            def select_stock(symbol):
                # hide StockSelector frame
                # if should_hide_when_selected is true
                if self.should_hide_when_selected is True:
                    print('removing stockresults frame')
                    self.sf_stock_results.grid_forget()

                # Run function, for example analysis or return stock name
                self.function_to_run(symbol)

            print('Button command, ', stock_results_dataframe['Symbol'][row_idx])
            # Create the select_stock_button and bind the custom made func to it
            select_button = tk.Button(inner_frame, text='Select stock',
                                      command=lambda symbol=stock_results_dataframe.iloc[row_idx]: select_stock(symbol))

            # Position the select_button with grid
            select_button.grid(row=row_idx * 2 + 2, column=0, padx=5, pady=10, sticky='w')

            # There are 6 data columns, iterate through each and add corresponding data
            for col_idx in range(6):
                # Add each stock as a row in a scrollable canvas
                # This: stock_results[row_idx][col_keys[col_idx]] gets the data value
                # for each stock and column
                info_label = tk.Label(inner_frame, text=stock_results_dataframe[col_keys[col_idx]][row_idx])

                # Place the info_label at the correct place. row_idx + 1 because
                # the first row is just column info. Second row is the first stock
                info_label.grid(row=row_idx * 2 + 2, column=col_idx + 1, padx=5, pady=10, sticky='w')
