# For GUI purposes
import tkinter as tk


# Self made modules, Like FundamentalAnalysisPage, TechnicalAnalysisPage and BetaRankingPage
from pages import *
from functional_frames import StockSelectorFrame


# Inspiration taken from: https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
class StockAnalysisApp(tk.Tk):

    # Initialize StockAnalysisApp class
    def __init__(self):

        # Initialize tkinter Tk class that this class inherits from
        tk.Tk.__init__(self)

        # Create a container that houses other frames/windows.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

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

# The actual program is run inside main()
def main():
    # Create the tkinter app window from the class called StockAnalysisApp()
    app = StockAnalysisApp()
    # Run the app
    app.mainloop()

# If this is run as file, not as an imported module. Start the program by running main()
if __name__ == "__main__":
    main()


# Copyright 2020 Oliver Midbrink
