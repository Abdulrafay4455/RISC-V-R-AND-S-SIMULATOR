# main.py
# This is the starting point of our project.
# Running this file will open the GUI window for the simulator.

import tkinter as tk
from gui import SimulatorGUI

if __name__ == "__main__":
    # creating the main tkinter window
    root = tk.Tk()

    # passing the window to our GUI class which builds everything
    app = SimulatorGUI(root)

    # this keeps the window open and listening for button clicks
    root.mainloop()
