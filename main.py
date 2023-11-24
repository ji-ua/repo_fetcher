#!/usr/bin/env python3

import tkinter as tk
from gui import GUI
  
def main():
    root = tk.Tk()
    root.title("github advanced search")
    app = GUI(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

if __name__ == "__main__":
    main()