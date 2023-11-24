#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Acquire repositories by conditional search. The format is json by default."""
__author__ = 'Jinya Nishi'
__version__ = '1.0.0'
__date__ = '2023/11/24 (Created:2023/11/24)'

import tkinter as tk
from gui import GUI
  
def main():
    """"mainn program."""
    
    root = tk.Tk()
    root.title("github advanced search")
    app = GUI(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

if __name__ == "__main__":
    main()