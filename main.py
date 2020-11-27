# For GUI purposes
import tkinter as tk


# Self made modules, Like FundamentalAnalysisPage, TechnicalAnalysisPage and BetaRankingPage
from pages import *
from functional_frames import StockSelectorFrame


# Inspiration taken from: https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# Class that houses the whole app, both the values/pages and also GUI Tk root.
# an instance of this class will be a full StockAnalysisApp app program windo
class StockAnalysisApp(tk.Tk):

    # Initialize StockAnalysisApp class
    def __init__(self):

        # Initialize tkinter Tk class that this class inherits from
        tk.Tk.__init__(self)

        # Create a container that houses other frames/windows.
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # This might need to change if something isnt working
        self.container.grid(row=0, column=0)

        # Variable to store all the frames
        self.frames = {}

        # Variable to store last frame
        self.last_frame = None

        # Tuple containing pages the StockAnalysisApp will use
        pages = (MenuPage, FundamentalAnalysisPage, TechnicalAnalysisPage, BetaRankingPage)

        # Create frames from all the pages (and set them up).
        # Also add them to the frames variable
        for Frame_name in pages:

            # create af frame using one of the pages
            # from "pages" as template
            frame = Frame_name(self.container, self)

            # Add the created frame to frames variable
            self.frames[Frame_name] = frame

        # Show the MenuPage as display
        self.display_frame(MenuPage)

    # Method that displays a certain frame based on the input argument container which will be one of the page classes.
    # The page class in the self.frames dictionary will be displayed
    # no return values, only container as argument
    def display_frame(self, container):
        if self.last_frame is not None:
            self.last_frame.grid_forget()

        # Choose the frame type specified in the function argument
        frame = self.frames[container]

        # Save the last frame
        self.last_frame = frame

        # Position the specified frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


# The main function will run the full program by creating an instance of the class stockAnalysisApp
# No inputted arguments required
# mostly to prevent program from being run as an imported module
# Could put the contents of main in if statement below.
def main():
    # Create the tkinter app window from the class called StockAnalysisApp()
    app = StockAnalysisApp()
    # Run the app
    app.mainloop()

# If this is run as file in the command line or IDE call the main function and start the app.
# Otherwise if this file is imported from another module. Do not run the app.
if __name__ == "__main__":
    main()


# Copyright 2020 Oliver Midbrink
