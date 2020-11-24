# Import GUI items
import tkinter as tk
from functional_frames import StockSelectorFrame, NavigationFrame

# For reading data about stocks such as balance sheet and historical prices
import yfinance as yf
from yahoofinancials import YahooFinancials

# For matrix operations on historic stock price data
import numpy as np

""" FUNCTIONS"""

# Technical analysis function that inputs some stock data as a dictionary
# with the mandatory 'Symbol' key inside. The symbol will be as standard in yahoo finance

# The function return a tuple containing the following data for the LAST 30 DAYS:
# Stock_price_change_in_percent during the latest 30 days
# Beta_value_as_defined_in_the_assignment (instead of traditional betavalue)
# lowest_price during these 30 days
# highest_price during last 30 days
def technical_analysis(stock_data):
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

    # Return the values calculated above in function. Order will be as defined in comment above function
    return (price_development_percentage, QUOTE_beta_value_UNQUOTE_for_stock, lowest_price, highest_price)


""" CLASSES """

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

# Fundamental analysis page template/class
class FundamentalAnalysisPage(tk.Frame):

    # Initialize FundamentalAnalysisPage
    def __init__(self, parent, controller):

        # Initialize parent class
        tk.Frame.__init__(self, parent)

        """" Navigation """

        navigation_frame = NavigationFrame(self, page_title="Fundamental Analysis",
                                            navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.present_fundamental_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def fundamental_analysis(self, stock_data):

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

    def present_fundamental_analysis(self, stock_data):

        # Using self.* in order to prevent duplicates when analysis is run multiple times

        # The method fundamental_analysis takes some time, so show a loading screen while we wait
        self.loading_label = tk.Label(self, text='Loading data...')
        self.loading_label.grid(row=2, column=1, padx=10, pady=10)

        # Try running the fundamental analysis, also except if there are errors
        try:
            # Run the fundamental_analysis method to retrieve fundamental key performance indicators
            equity_ratio, price_per_earnings, price_per_revenue = self.fundamental_analysis(stock_data)

            print('Ran fundamental analysis with:', stock_data['Symbol'])

            # Present the values
            # Label showing what company has been analyzed
            self.company_label = tk.Label(self, text="Fundamental Analysis for:  "+stock_data['Name'], font=('Times', 16, 'bold'))
            self. company_label.grid(row=2, column=1, padx=10, pady=10, sticky='w')

            # Label for equity ratio round to 3 decimals
            self.equity_ratio_label = tk.Label(self, text="Equity ratio (Soliditet): " + str(round(equity_ratio, 3)))
            self.equity_ratio_label.grid(row=3, column=1, padx=10, pady=10, sticky='w')

            # Label for price per earnings round to 3 decimals
            self.price_per_earnings_label = tk.Label(self, text="Price per earnings (P/E): " + str(round(price_per_earnings, 3)))
            self.price_per_earnings_label.grid(row=4, column=1, padx=10, pady=10, sticky='w')

            # Label for price per revenue round to 3 decimals
            self.price_per_revenue_label = tk.Label(self, text="Price per revenue (P/S): " + str(round(price_per_revenue, 3)))
            self.price_per_revenue_label.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        except Exception as e:
            # If something goes wrong in the fundamental_analysis tell the user that an error occured

            # Error label
            self.error_label = tk.Label(self, text="Something went wrong with the fundamental analysis", font=('Times', 16, 'bold'))
            self.error_label.grid(row=2, column=1, padx=10, pady=10, sticky='w')

            # Describe what went wrong
            self.error_description_label = tk.Label(self, text="Error description: " + str(e))
            self.error_description_label.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Finally remove the loading label once the values have been retrieved and calculated
        self.loading_label.grid_forget()


# Technical analysis page for
class TechnicalAnalysisPage(tk.Frame):

    # Initialize TechnicalAnalysisPage
    def __init__(self, parent, controller):

        # Initialize parent class
        tk.Frame.__init__(self, parent)

        """" Navigation """

        navigation_frame = NavigationFrame(self, page_title="Technical Analysis",
                                           navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.present_technical_analysis, controller, True)

        # Position the StockSelector frame
        stock_selector.grid(row=1, column=1, sticky="nsew")


    def present_technical_analysis(self, stock_data):
        price_development, QUOTE_betavalue_UNQUOTE, lowest_price, highest_price = technical_analysis(stock_data)
        print('Ran technical analysis with: ', stock_data['Symbol'])

        # Present values




class BetaRankingPage(tk.Frame):

    # Initialize BetaRankingPage
    def __init__(self, parent, controller):
        # Initialize parent class
        tk.Frame.__init__(self, parent)

        # List to keep track of which stocks should be compared
        self.stocks_to_compare = []

        """" Navigation """

        navigation_frame = NavigationFrame(self, page_title="Stocks ranked by beta value",
                                           navigation_command=lambda: controller.display_frame(MenuPage))
        navigation_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        """ Content """

        # Create a stock selector window to let user select a stock and run the specified function with it
        stock_selector = StockSelectorFrame(self, self.add_stock_to_ranking_list, controller, False)

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

    def add_stock_to_ranking_list(self, stock_data):
        # Add stock only if not already added to comparison list
        if stock_data['Symbol'] not in self.stocks_to_compare:
            print('Added ', stock_data['Symbol'], ' to beta list.')
            self.stocks_to_compare.append(stock_data['Symbol'])

            # Add list item of the current selected stock to the total list of selected stocks
            row_text = stock_data['Symbol'] + ' - ' + stock_data['Name']
            stock_label = tk.Label(self.beta_rank_frame, text=row_text)

            stock_label.grid(row=1 + len(self.stocks_to_compare), column=1, padx=10, pady=10, sticky='w')
        else:
            print('Symbol ', stock_data['Symbol'], ' already added to beta list.')
