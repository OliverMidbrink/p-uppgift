# Import GUI items
import tkinter as tk
from functional_frames import StockSelectorFrame, NavigationFrame, ListFrame

# For reading data about stocks such as balance sheet and historical prices
import yfinance as yf
from yahoofinancials import YahooFinancials

# For matrix operations on historic stock price data
import numpy as np

""" FUNCTIONS"""

# Technical analysis function that inputs some stock data as a dictionary
# with the mandatory 'Symbol' key inside. The symbol will be as standard in yahoo finance. for example 'AAPL'

# The function returns a tuple containing the following data in the form of floats for the LAST 30 DAYS:
# Stock_price_change_in_percent during the latest 30 days
# Beta_value_as_defined_in_the_assignment (instead of traditional betavalue)
# lowest_price during these 30 days
# highest_price during last 30 days
# currency of stock (in the form of a string)

# If an error occurs the function will return None
def technical_analysis(stock_data):
    # Added try catch to catch errors
    try:
        # Run technical analysis

        # Retrieve a data frame containing the stock price for the latest 30 days
        stock_prices_latest_30_days = yf.download(stock_data['Symbol'], period='1mo')
        print('Dataframe: ', stock_prices_latest_30_days)
        print('Close: ', stock_prices_latest_30_days['Close'])
        print('Open: ', stock_prices_latest_30_days['Open'])

        # Get the opening price from 30 days ago using pandas dataframe indexing
        stock_price_30_days_ago = stock_prices_latest_30_days['Open'][0]
        print('Price 30 days ago: ', stock_price_30_days_ago)

        # Get the latest price
        stock_price_latest_close = stock_prices_latest_30_days['Close'][-1]
        print('Latest closing price: ', stock_price_latest_close)

        # Calculate price development during 30 latest days
        price_development_percentage = (stock_price_latest_close / stock_price_30_days_ago - 1) * 100
        print('Price development %: ', price_development_percentage)

        # Calculate highest price during latest 30 days
        highest_price = np.amax(stock_prices_latest_30_days['High'])
        print('Highest_price latest 30 days: ', highest_price)

        # Calculate lowest price during latest 30 days
        lowest_price = np.amin(stock_prices_latest_30_days['Low'])
        print('Lowest_price latest 30 days: ', lowest_price)

        # Calculate "betavärde" for a this stock. "betavärde" is
        # Get a Ticker object that can retrieve information about a market index
        dow_jones_ticker = yf.Ticker('^DJI')
        dow_jones_data = dow_jones_ticker.history()

        print(dow_jones_data)

        # Dow jones price 30 days ago
        dow_jones_price_30_days_ago = dow_jones_data['Open'][0]

        # Dow jones price around now
        dow_jones_price_latest_close = dow_jones_data['Close'][-1]

        # "beta value" for this is calculated as:
        # (stock_price_now / old_stock_price) / (index_price_now / old_index_price)
        # Where the old price represents the price approximately 30 days ago depending
        # when the market open days are
        QUOTE_beta_value_UNQUOTE_for_stock = (stock_price_latest_close / stock_price_30_days_ago) / (
                    dow_jones_price_latest_close / dow_jones_price_30_days_ago)

        print('"Beta value": ', QUOTE_beta_value_UNQUOTE_for_stock)

        # Get currency for stock
        stock_ticker = yf.Ticker(stock_data['Symbol'])

        # Get stock currency
        currency = stock_ticker.info['currency']
        print('Currency: ', currency)


        # Return the values calculated above in function. Order will be as defined in comment above function
        return (price_development_percentage, QUOTE_beta_value_UNQUOTE_for_stock, lowest_price, highest_price, currency)
    except Exception as e:
        print('Error: ', e)

    return None


# Input: dictionary with 'Symbol' key that corresponds to the yahoo symbol string used in their API and website.
# For example 'AAPL' or 'SAAX' or 'VOLV-B.ST'
# The method will the caluclate a set of fundamental values. The equity ratio, price_per_earnings for the
# company (not stock), and lastly price per revenue (also for company).
# The output will be a tuple of consisting of these values represented as floats.
def fundamental_analysis(stock_data):

    # Run fundamental analysis

    # Get stock balance sheet
    yahoo_financials = YahooFinancials(stock_data['Symbol'])
    raw_balance_sheet = yahoo_financials.get_financial_stmts('annual', 'balance')

    # Calculate solidity
    print('balance_sheet ', raw_balance_sheet)

    # Get the balance_sheet for latest fiscal year
    balanceSheetHistory_for_stock = raw_balance_sheet['balanceSheetHistory'][stock_data['Symbol']][0]
    balance_sheet_latest_year_for_this_stock = balanceSheetHistory_for_stock[list(balanceSheetHistory_for_stock.keys())[0]]

    total_shareholder_equity = balance_sheet_latest_year_for_this_stock['totalStockholderEquity']
    total_assets = balance_sheet_latest_year_for_this_stock['totalAssets']

    # Equity ratio ~ soliditet
    equity_ratio = total_shareholder_equity / total_assets
    print('Equity ratio: ', equity_ratio)

    # Calulate p/e

    # Get income statement to read earnings value
    raw_income_statement = yahoo_financials.get_financial_stmts('annual', 'income')['incomeStatementHistory'][stock_data['Symbol']][0]
    income_statement_latest_year_for_this_stock = raw_income_statement[list(raw_income_statement.keys())[0]]
    print('raw_income_statement', raw_income_statement)


    # Get net income for the latest fiscal year
    net_income = income_statement_latest_year_for_this_stock['netIncome']
    print('Net income: ', net_income)
    print('Shareholder Equity: ', total_shareholder_equity)


    # Calculate price per earnings by dividing total shareholder equity by net income
    price_per_earnings = total_shareholder_equity / net_income
    print('Price per earnings: ', price_per_earnings)

    # Calculate price per revenue by dividing total shareholder equity with total_revenue
    total_revenue = income_statement_latest_year_for_this_stock['totalRevenue']
    price_per_revenue = total_shareholder_equity / total_revenue

    print(price_per_revenue)

    return (equity_ratio, price_per_earnings, price_per_revenue)

""" CLASSES """

# Define the menu page template
class MenuPage(tk.Frame):

    # Initialize the MenuPage, parent will be the StockAnalysisApps in this case (the parent frame or tkinter object)
    # container. Controller will be a tk.Tk object defined by StockAnalysisApp and will control which views is presented
    # to the user, hence the name controller.
    def __init__(self, parent, controller):

        # Initialize parent class/standard tkinter frame initialization.
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


# Fundamental analysis page template/class
class FundamentalAnalysisPage(tk.Frame):

    # Initialize FundamentalAnalysisPage
    # Input is the parent tkinter object
    # Controller will be the tkinter object controlling the choice of page. In this case StockAnalysisApp.
    def __init__(self, parent, controller):

        # Initialize parent class/standard tkinter frame initialization.
        tk.Frame.__init__(self, parent)

        """" Navigation """
        # use a navigation frame obects as described in functional_frames
        navigation_frame = NavigationFrame(self, page_title="Fundamental Analysis",
                                            navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.present_fundamental_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    # A function that calls the fundamental_analysis function and retrieves appropriate fundamental values.
    # The values will be displayed using the ListFrame class from functional frames.
    # Input is the stock_data dictionary with keys 'Symbol' and 'Name' that contains the stock symbol and
    # the stock/company name respectively.
    # No values are returned. Results will be displayed in GUI
    def present_fundamental_analysis(self, stock_data):

        # Using self.* in order to prevent duplicates when analysis is run multiple times

        # The method fundamental_analysis takes some time, so show a loading screen while we wait
        self.loading_label = tk.Label(self, text='Loading data...')
        self.loading_label.grid(row=2, column=0, padx=10, pady=10)

        # Try running the fundamental analysis, also except if there are errors
        try:
            # Run the fundamental_analysis method to retrieve fundamental key performance indicators
            equity_ratio, price_per_earnings, price_per_revenue = fundamental_analysis(stock_data)

            print('Ran fundamental analysis with:', stock_data['Symbol'])

            # Present the values
            # Label showing what company has been analyzed

            # Title for the list_frame_class
            list_frame_title = "Fundamental Analysis for:  " + stock_data['Name']

            # Data containing strings for the list_frame_class. All rounded to 3 decimals
            list_frame_data = [
                "Yahoo Finance Symbol is:\t" + stock_data['Symbol'],
                "Equity ratio (Soliditet):\t" + str(round(equity_ratio * 100, 3)) + "%",
                "Price per earnings (P/E):\t" + str(round(price_per_earnings, 3)),
                "Price per revenue (P/S):\t" + str(round(price_per_revenue, 3))
            ]

            # Create a listFrame to show all the data in a convenient manner
            self.list_frame = ListFrame(self, list_frame_title, list_frame_data)
            self.list_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')


        except Exception as e:
            # If something goes wrong in the fundamental_analysis tell the user that an error occured

            # Error label
            self.error_label = tk.Label(self, text="Something went wrong with the fundamental analysis", font=('Times', 16, 'bold'))
            self.error_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

            # Describe what went wrong
            self.error_description_label = tk.Label(self, text="Error description: " + str(e))
            self.error_description_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Finally remove the loading label once the values have been retrieved and calculated
        self.loading_label.grid_forget()


# Technical analysis page for
class TechnicalAnalysisPage(tk.Frame):

    # Initialize TechnicalAnalysisPage
    # Parent and controller are defined in other pages. Parent is parent tkinter container/frame and controller
    # is Stockanalysis app in this case
    def __init__(self, parent, controller):

        # Initialize parent class/standard tkinter frame initialization.
        tk.Frame.__init__(self, parent)

        """" Navigation """
        # use a navigation frame obects as described in functional_frames
        navigation_frame = NavigationFrame(self, page_title="Technical Analysis",
                                           navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.present_technical_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # A function that will display some gathered technical values that are retrieved from the
    # technical_analysis_function. If the value returned from the technical_analysis function are None istead of a tuple
    # present that an error occured to the user. Otherwise use a ListFrame object (see functional_frames) in order
    # to display the data.
    #
    # This function takes in a dictionary stock_data as standard with the keys 'Symbol' and 'Name' that corresponds to
    # the stock symbol string and stock name string. The format of these will be as the standard in yahoo finance
    # Apple symbol string is 'AAPL' for example and their name is 'Apple Inc.'
    #
    # This function returns nothing. Only the GUI is updated for the user.
    def present_technical_analysis(self, stock_data):
        # Get technical_values
        technical_values = technical_analysis(stock_data)

        # If there was no error unpack the technical values and continue
        if technical_values is not None:
            price_development, QUOTE_betavalue_UNQUOTE, lowest_price, highest_price, currency = technical_values
            print('Ran technical analysis with: ', stock_data['Symbol'])

            # Present values with a list frame

            # Create list frame title
            list_frame_title = "Technical Analysis with: \t" + stock_data['Name']

            # Create list frame data
            list_frame_data = [
                "Yahoo Finance Symbol is:\t\t\t\t\t\t" + stock_data['Symbol'],
                "Price development of stock during last 30 days:\t\t\t\t" + str(round(price_development, 3)) + '%',
                "Betavalue as defined in assignment last 30 days, compared to DOW JONES: \t" + str(round(QUOTE_betavalue_UNQUOTE, 3)),
                "Lowest stock price during last 30 days:\t\t\t\t\t" + currency + ' ' + str(round(lowest_price, 3)),
                "Highest stock price during last 30 days:\t\t\t\t\t" + currency + ' ' + str(round(highest_price, 3))
            ]


            # Create a listFrame to show all the data in a convenient manner
            self.list_frame = ListFrame(self, list_frame_title, list_frame_data)
            self.list_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        else:
            # There was an error with the technical_analysis. Could be lots of reasons

            # Tell the user there was an error
            error_label = tk.Label(self,
                                   text="An error occured when running the technical analysis for stock with symbol: " +
                                   stock_data['Symbol'])
            # position the error label
            error_label.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

# A class that defines the beta_value ranking of stocks as defined in the assignment
# It will let the user enter a number of stocks and will then attempt to compare these stocks
# if there is no data for a particular stock it will have Error in its name and be ranked at the bottom (
# since its beta_value is 0)
# The class will inherit from the tk.Frame object as usual with the other pages in this project
class BetaRankingPage(tk.Frame):

    # Initialize BetaRankingPage, parent is the parent frame and controller is the StockAnalysis app
    def __init__(self, parent, controller):
        # Initialize parent class
        tk.Frame.__init__(self, parent)

        """" Navigation """
        # use standard navigation_frame for page title and back to menu button
        navigation_frame = NavigationFrame(self, page_title="Stocks ranked by beta value - Select a few to compare",
                                           navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=1, sticky="ew")

        """ Content """

        # Create a selected stocks frame from scratch
        self.start_or_restart_selected_stocks_frame()

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.add_stock_to_ranking_list, controller, False)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create a frame to house compare and reset buttons
        button_frame = tk.Frame(self)
        # Compare stocks button
        compare_stock_button = tk.Button(button_frame, text="Compare stocks", command=self.compare_stocks)

        # Position compare button
        compare_stock_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Reset button
        reset_button = tk.Button(button_frame, text="Restart Comparison", command=self.start_or_restart_selected_stocks_frame)

        # Position reset button
        reset_button.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # position button frame
        button_frame.grid(row=0, column=1, sticky='nswe')

    # This is the function that both initializes the selected stocks frame on the right of the beta_value ranking page.
    # It will empty all the list objects containing the stocks and corresponding descriptions to be compared.
    # Also the fucntion will create ad new stocks_to_compare frame so that it is clean and fresh witout old labels.
    # This will be easier for the user.
    # The method takes no arguments except the self arg and returns nothing.
    def start_or_restart_selected_stocks_frame(self):
        # List to keep track of which stock symbols should be compared
        self.stock_symbols_to_compare = []

        # List to keep track of stock names or identifiers
        self.stock_identifiers = []

        # Contain all beta rank presentation within a list frame
        self.stocks_to_compare_frame = self.create_stocks_to_compare_frame()

    # This function creates a new stocks_to compare frame heavily based on the listFrame object form function_frames.
    # It sets the title to "Selected Stocks" and the data will be the self.stock_identifiers.
    # This variable will contain the stock symbol and name.
    # The function returns this newly created ListFrame object
    def create_stocks_to_compare_frame(self):
        return ListFrame(self, 'Selected stocks', self.stock_identifiers, font=('Courier', 12, 'normal')).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # This function will add a stock to the list of stocks to be compared when the user hits a select stock button
    # in the select stocks. The data added when a "select stock" button is pressed will be the stock symbol and
    # an identifier string will be created.
    # The function takes the stock_data as input. A dictionary containing the keys 'Symbol' And 'Name' containing
    # strings of symbol and company/symbol name respectively.
    # The function returns no values
    def add_stock_to_ranking_list(self, stock_data):
        # Add stock only if not already added to comparison list
        if stock_data['Symbol'] not in self.stock_symbols_to_compare:
            print('Added ', stock_data['Symbol'], ' to beta list.')
            self.stock_symbols_to_compare.append(stock_data['Symbol'])

            # Add a description to stock_identifiers list about this stock
            row_text = 'Symbol: ' + stock_data['Symbol'] + ' - Name: ' + stock_data['Name']
            self.stock_identifiers.append(row_text)
        else:
            print('Symbol ', stock_data['Symbol'], ' already added to beta list.')

        print(self.stock_symbols_to_compare)
        print(self.stock_identifiers)

        # Update selected stocks frame
        self.stocks_to_compare_frame = self.create_stocks_to_compare_frame()

    # This function will compare the stocks that have been selected by the user. This is done by running a
    # technical_analysis for each stock symbol and the sorting a list of all the stocks based on the highest beta_value
    # first. The function will use the attributes self.stock_symbols_to_compare and self.stock_identifiers in order to
    # know which stocks to compare.
    # No arguments except self
    # No return values
    def compare_stocks(self):
        print('Comparing stocks: ', self.stock_symbols_to_compare)

        # List containing "betavalue" and symbol
        beta_and_symbol_list = []

        # Generate list with stock symbol and "betavalue" as elements
        for stock_idx in range(len(self.stock_symbols_to_compare)):
            # Create the proper data structure for the technical_analysis function
            stock_data = {'Symbol': self.stock_symbols_to_compare[stock_idx]}

            # Run the technical_analysis function and apply the return values to tuple technical_values
            technical_values = technical_analysis(stock_data)

            # Set the "betavalue" in case there was an error with technical_analysis()
            QUOTE_betavalue_UNQOUTE = 0

            stock_description = 'Error for this stock: ' + self.stock_identifiers[stock_idx]

            # Set values only if there was no error
            if technical_values is not None:
                # "betavalue" will be the second return value
                QUOTE_betavalue_UNQOUTE = technical_values[1]

                # set stock description value
                stock_description = self.stock_identifiers[stock_idx]



            # Add three values to the beta_and_symbol list. Stock symbol, "betavalue" and stock description (identifier)
            beta_and_symbol_list.append((self.stock_symbols_to_compare[stock_idx],
                                         QUOTE_betavalue_UNQOUTE,
                                         stock_description))

        beta_and_symbol_list.sort(key=lambda x: x[1], reverse=True)
        print('Sorted beta list: ', beta_and_symbol_list)

        # Create a list for the list frame
        beta_info_list = []

        # Iterate through the sorted beta_and_symbol_list in order to prepara a data list for a list frame
        stock_rank_according_to_beta = 1
        for stock_info in beta_and_symbol_list:
            # Append all the stocks to the final list frame data list that will be displayed to user
            # First present rank then present beta then present stock information
            beta_info_list.append(str(stock_rank_according_to_beta) + '. ' + 'Beta: ' +
                                  str(round(stock_info[1], 3)) + ' - ' + stock_info[2])

            # Add to the rank through each iteration so that the ranks are increasing
            stock_rank_according_to_beta += 1


        # If there were no stocks selected, ask user to select stocks
        if len(self.stock_symbols_to_compare) is 0:
            # Add text to beta_info_list that will be displayed
            # Message to be added is that the user has to choose stocks

            beta_info_list.append('Please select stocks to run analysis. Press restart then choose stocks. ')


        # Create a listframe to display all the beta ranking data
        self.stocks_to_compare_frame = ListFrame(self, 'Ranking according to "betavalue"', beta_info_list,
                                                 font=('Courier', 10, 'normal')).grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew"
        )


# Copyright 2020 Oliver Midbrink