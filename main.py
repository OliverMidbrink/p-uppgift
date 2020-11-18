# For GUI purposes
import tkinter as tk
from tkinter import ttk
from tkscrolledframe import ScrolledFrame
from tkinter.ttk import *

# For reading data about stocks such as balance sheet and historical prices
import yfinance as yf

# Mostly for web-scraping used in the StockSelector search_stock method
import requests
import re   # For example escaping special characters in string
from bs4 import BeautifulSoup

# Inspiration taken from: https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
class StockAnalysisApp(tk.Tk):

    # Initialize StockAnalysisApp class
    def __init__(self):

        # Initialize tkinter Tk class that this class inherits from
        tk.Tk.__init__(self)

        # Create a container that houses other frames/windows.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        # This might need to change if something isnt working
        container.grid(row=0, column=0)

        # Variable to store all the frames
        self.frames = {}

        # Tuple containing pages the StockAnalysisApp will use
        pages = (MenuPage, FundamentalAnalysisPage, TechnicalAnalysisPage, BetaRankingPage)

        # Create frames from all the pages (and set them up).
        # Also add them to the frames variable
        for Frame_name in pages:

            # create af frame using one of the pages
            # from "pages" as template
            frame = Frame_name(container, self)

            # Position the created frame
            frame.grid(row=0, column=0, sticky="nsew")

            # Add the created frame to frames variable
            self.frames[Frame_name] = frame

        # Show the MenuPage as display
        self.display_frame(MenuPage)

    # Display the frame that was passed as a parameter
    # Do this by getting the corresponding frame from
    # the self.frames variable
    def display_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


# Define the menu page template
class MenuPage(tk.Frame):

    # Initialize the MenuPage, parent will be the StockAnalysisApps
    # container. Controller will be a tk.Tk object defined by StockAnalysisApp
    def __init__(self, parent, controller):

        # Initialize class that MenuPage inherits from
        tk.Frame.__init__(self, parent)

        # Page title
        title = tk.Label(self, text='Stock Analysis App', font=("Times", 20, "bold"))
        title.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Subheading
        subheading = tk.Label(self, text='Please choose an option below:', font=("Times", 15, "normal"))
        subheading.grid(row=1, column=1, padx=10, pady=10, sticky="nw")


        # Fundamental analysis button shows fundamental analysis
        fundamental_analysis_button = tk.Button(self, text='Run Fundamental Analysis',
            command=lambda: controller.display_frame(FundamentalAnalysisPage))

        # position fundamental analysis button
        fundamental_analysis_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")


        # Technical analysis button shows technical analysis
        technical_analysis_button = tk.Button(self, text='Run Technical Analysis',
            command=lambda: controller.display_frame(TechnicalAnalysisPage))

        # position technical analysis button
        technical_analysis_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")


        # Beta ranking button shows beta ranking
        beta_ranking_button = tk.Button(self, text='Rank stocks with regard to beta value',
            command=lambda: controller.display_frame(BetaRankingPage))

        # position beta ranking button button
        beta_ranking_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")


# StockSelector is a frame that lets the user choose a stock
class StockSelector(tk.Frame):

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
        search_label = tk.Label(self, text="Search Stock: ")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # Searchfield for stock keyword
        search_bar = tk.Entry(self)
        search_bar.grid(row=0, column=1, padx=10, pady=10)
        # Save search_bar as attribute
        self.search_bar = search_bar

        # Search button that when pressed, feeds the
        # string from search_bar to search_stock method as well as
        # should_hide_when_selected.
        # search function written here for clarity
        def search_function():
            self.display_search_results(self.search_stock(search_bar.get()))

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

    def display_search_results(self, stock_results):
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
        if len(stock_results) > 0:
            col_names = ['Select Stock', 'Symbol', 'Name', 'Last Price', 'Industry/Category', 'Type', 'Exchange']
            for col_idx in range(len(col_names)):
                col_label = tk.Label(inner_frame, text=col_names[col_idx], font=('Arial', 15, 'bold'))
                col_label.grid(row=0, column=col_idx, sticky='w')
        # Otherwise tell user there were no results
        else:
            no_results_label = tk.Label(inner_frame, text='No search reults for keyword: ' + self.search_bar.get())
            no_results_label.grid(row=0, column=0, sticky='w')

        # Here are the column keys
        col_keys = ['symbol', 'name', 'last_price', 'industry_or_category', 'type', 'exchange']

        # Iterate through rows and columns and add all data for resulting stocks
        for row_idx in range(len(stock_results)):

            # Separate rows for easier navigation using separator class
            Separator(inner_frame, orient='horizontal').grid(row=row_idx * 2 + 1,
                                                             column=0,
                                                             sticky='ew',
                                                             columnspan=7
                                                             )
            # Create select stock button for each row
            this_stock_symbol = stock_results[row_idx]['symbol']

            # Function that runs this stock_selectors function_to_run with
            # the selected stock.
            def assigned_func(stock_data):
                # Run function, for example analysis or return stock name
                self.function_to_run(stock_data)

                # After running function_to_run, hide StockSelector frame
                # if should_hide_when_selected is true
                if self.should_hide_when_selected is True:
                    self.sf_stock_results.grid_forget()

            # Create the select_stock_button and bind the custom made func to it
            select_button = tk.Button(inner_frame, text='Select stock',
                                      command=lambda stock_data=stock_results[row_idx]: assigned_func(stock_data))

            # Position the select_button with grid
            select_button.grid(row=row_idx * 2 + 2, column=0, padx=5, pady=10, sticky='w')

            # There are 6 data columns, iterate through each and add corresponding data
            for col_idx in range(6):
                # Add each stock as a row in a scrollable canvas
                # This: stock_results[row_idx][col_keys[col_idx]] gets the data value
                # for each stock and column
                info_label = tk.Label(inner_frame, text=stock_results[row_idx][col_keys[col_idx]])

                # Place the info_label at the correct place. row_idx + 1 because
                # the first row is just column info. Second row is the first stock
                info_label.grid(row=row_idx * 2 + 2, column=col_idx + 1, padx=5, pady=10, sticky='w')


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

        # List for storing stock results from search
        stock_results = []

        # Iterate through search results and create info dictionaries for each
        # result. Then filter only for stocks by adding only stocks to stock_results
        for result in all_html_results:

            # Dictionary for storing information for this current result
            # (that will be of type STOCK or ETF or MUTUAL FUND or other)
            result_info = {}

            # Get all the html columns of this result
            columns = result.find_all('td')

            # Get the symbol name of result
            result_info['symbol'] = columns[0].find('a').get_text()

            # Get the name of result
            result_info['name'] = columns[1].get_text()

            # Get the Last price of result
            result_info['last_price'] = columns[2].get_text()

            # Get the industry of the result
            result_info['industry_or_category'] = columns[3].get_text()

            # Get the type of the result (for example stock or etf)
            result_info['type'] = columns[4].get_text()

            # Get the Exchange that trades this result
            result_info['exchange'] = columns[5].get_text()

            # Log information about this financial item result
            #self.log_financial_item_info(result_info)

            # If the search result is a stock, add its data to stock_results
            if 'Stocks' in result_info['type']:
                stock_results.append(result_info)

        return stock_results


# Fundamental analysis page template/class
class FundamentalAnalysisPage(tk.Frame):

    # Initialize FundamentalAnalysisPage
    def __init__(self, parent, controller):

        # Initialize parent class
        tk.Frame.__init__(self, parent)

        """" Navigation """

        # Page title
        title = tk.Label(self, text="Fundamental Analysis", font=("Times", 16, "bold"))
        title.grid(row=0, column=4, padx=10, pady=10)

        # Back to menu button
        back_button = tk.Button(self, text="Back to Main Menu",
                                command=lambda : controller.display_frame(MenuPage))
        back_button.grid(row=0, column=0, padx=10, pady=10)

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelector(self, self.present_fundamental_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=1, sticky="nsew")

    def fundamental_analysis(self, stock_data):
        # Run fundamental analysis
        pass
    
    def present_fundamental_analysis(self, stock_data):
        fundamental_values = self.fundamental_analysis(stock_data['symbol'])
        print('Ran fundamental analysis with: ', stock_data['symbol'])
        #present values



class TechnicalAnalysisPage(tk.Frame):

    # Initialize TechnicalAnalysisPage
    def __init__(self, parent, controller):

        # Initialize parent class
        tk.Frame.__init__(self, parent)

        """" Navigation """

        # Page title
        title = tk.Label(self, text="Technical Analysis", font = ("Times", 16, "bold"))
        title.grid(row=0, column=4, padx=10, pady=10)

        # Back to menu button
        back_button = tk.Button(self, text="Back to Main Menu",
                                command=lambda: controller.display_frame(MenuPage))
        back_button.grid(row=0, column=0, padx=10, pady=10)

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelector(self, self.present_technical_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=1, sticky="nsew")

    def technical_analysis(self, stock_data):
        # Run technical analysis
        pass

    def present_technical_analysis(self, stock_data):
        technical_values = self.technical_analysis(stock_data['symbol'])
        print('Ran technical analysis with: ', stock_data['symbol'])
        # Present values




class BetaRankingPage(tk.Frame):

    # Initialize BetaRankingPage
    def __init__(self, parent, controller):
        # Initialize parent class
        tk.Frame.__init__(self, parent)

        # List to keep track of which stocks should be compared
        self.stocks_to_compare = []

        """" Navigation """

        # Page title
        title = tk.Label(self, text="Stocks ranked by beta value", font = ("Times", 16, "bold"))
        title.grid(row=0, column=4, padx=10, pady=10)

        # Back to menu button
        back_button = tk.Button(self, text="Back to Main Menu",
                                command=lambda: controller.display_frame(MenuPage))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelector(self, self.add_stock_to_ranking_list, controller, False)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=0, sticky="nsew")

        # Contain all beta rank presentation within a frame
        beta_rank_frame = tk.Frame(self)
        beta_rank_frame.grid(row=1, column=1, sticky="nsew")
        # Save as attribute
        self.beta_rank_frame = beta_rank_frame

        # Label to show which stocks are selected underneath
        selected_stocks_label = tk.Label(beta_rank_frame, text='Selected Stocks', font=('times', 15, 'bold'))

        # Position selected_stocks_label
        selected_stocks_label.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        # Add separators to clarify

    def add_stock_to_ranking_list(self, stock_data):
        # Add stock only if not already added to comparison list
        if stock_data['symbol'] not in self.stocks_to_compare:
            print('Added ', stock_data['symbol'], ' to beta list.')
            self.stocks_to_compare.append(stock_data['symbol'])

            # Add list item of the current selected stock to the total list of selected stocks
            row_text = stock_data['symbol'] + ' - ' + stock_data['name']
            stock_label = tk.Label(self.beta_rank_frame, text=row_text)

            stock_label.grid(row=1 + len(self.stocks_to_compare), column=1, padx=10, pady=10, sticky='w')
        else:
            print('Symbol ', stock_data['symbol'], ' already added to beta list.')



# The actual program is run inside main()
def main():
    # Create the tkinter app window from the class called StockAnalysisApp()
    app = StockAnalysisApp()
    # Run the app
    app.mainloop()

# If this is run as file, not as an imported module. Start the program by running main()
if __name__ == "__main__":
    main()