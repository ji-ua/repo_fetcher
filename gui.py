#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import calendar

from fetcher import Fetcher

class GUI(tk.Frame):
    """GUI:enter query parameters."""

    def __init__(self, parent, *args, **kwargs):
        """constructor of GUI."""
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_ui()
        self.set_dafault_values()

    def setup_ui(self):
        """set UI."""
        min_fork_row = 1
        max_fork_row= 2
        before_date_row = 3
        after_date_row = 4
        topic_row = 5
        archived_row = 6
        format_row = 7
        filename_row = 8
        send_row = 10

        tk.Label(self, text="最小フォーク数").grid(row=min_fork_row, column=0)
        self.forks_min_entry = tk.Entry(self)
        self.forks_min_entry.grid(row=min_fork_row, column=1)

        tk.Label(self, text="最大フォーク数").grid(row=max_fork_row, column=0)
        self.forks_max_entry = tk.Entry(self)
        self.forks_max_entry.grid(row=max_fork_row, column=1)

        tk.Label(self, text="更新日の上限").grid(row=before_date_row, column=0)
        self.before_year_var = tk.StringVar()
        year_before_combobox = ttk.Combobox(self, textvariable=self.before_year_var, values=[i for i in range(2008, 2031)])
        year_before_combobox.grid(row=before_date_row, column=1)
        year_before_combobox.bind('<<ComboboxSelected>>', lambda event: self.update_days(type='before'))

        self.before_month_var = tk.StringVar()
        month_before_combobox = ttk.Combobox(self, textvariable=self.before_month_var, values=[i for i in range(1, 13)])
        month_before_combobox.grid(row=before_date_row, column=2)
        month_before_combobox.bind('<<ComboboxSelected>>', lambda event: self.update_days(type='before'))

        self.before_day_var = tk.StringVar()
        self.before_day_combobox = ttk.Combobox(self, textvariable=self.before_day_var, values=[])
        self.before_day_combobox.grid(row=before_date_row, column=3)

        tk.Label(self, text="更新日の下限").grid(row=after_date_row, column=0)
        self.after_year_var = tk.StringVar()
        year_after_combobox = ttk.Combobox(self, textvariable=self.after_year_var, values=[i for i in range(2008, 2031)])
        year_after_combobox.grid(row=after_date_row, column=1)
        year_after_combobox.bind('<<ComboboxSelected>>', lambda event: self.update_days(type='after'))

        self.after_month_var = tk.StringVar()
        month_after_combobox = ttk.Combobox(self, textvariable=self.after_month_var, values=[i for i in range(1, 13)])
        month_after_combobox.grid(row=after_date_row, column=2)
        month_after_combobox.bind('<<ComboboxSelected>>', lambda event: self.update_days(type='after'))

        self.after_day_var = tk.StringVar()
        self.after_day_combobox = ttk.Combobox(self, textvariable=self.after_day_var, values=[])
        self.after_day_combobox.grid(row=after_date_row, column=3)

        tk.Label(self, text="トピック").grid(row=topic_row, column=0)
        self.topic_entry = tk.Entry(self)
        self.topic_entry.grid(row=topic_row, column=1)

        tk.Label(self,text="アーカイブされているか").grid(row=archived_row, column=0)
        self.archived_var = tk.StringVar()
        self.archived_var.set("false")
        archived = ["ture", "false"]
        tk.OptionMenu(self, self.archived_var, *archived).grid(row=archived_row, column=1)
        
        tk.Label(self, text="出力フォーマット（デフォルト:json）").grid(row=format_row, column=0)
        self.format_var = tk.StringVar()
        self.format_var.set("json")  # デフォルト値
        formats = ["json"]
        tk.OptionMenu(self, self.format_var, *formats).grid(row=format_row, column=1)

        tk.Label(self, text="出力ファイル名（拡張子なし）").grid(row=filename_row, column=0)
        self.filename_entry = tk.Entry(self)
        self.filename_entry.grid(row=filename_row, column=1)

        self.bind('<Return>', self.on_submit)
        submit_button = tk.Button(self, text="クエリ送信", command=self.on_submit)
        submit_button.grid(row=send_row, column=2)
   
    def update_days(self, type):
        """upadte days."""
        if type == 'before':
            year = int(self.before_year_var.get())
            month = int(self.before_month_var.get())
            last_day = calendar.monthrange(year, month)[1]
            self.before_day_combobox['values'] = [i for i in range(1, last_day + 1)]
        
        if type == 'after':
            year = int(self.after_year_var.get())
            month = int(self.after_month_var.get())
            last_day = calendar.monthrange(year, month)[1]
            self.after_day_combobox['values'] = [i for i in range(1, last_day + 1)]

    
    def set_dafault_values(self):
        """set default parameters."""
        self.forks_min_entry.delete(0, tk.END)
        self.forks_max_entry.delete(0, tk.END)
        self.before_year_var.set("2023")
        self.before_month_var.set("1")
        self.before_day_var.set("1")
        self.after_year_var.set("2023")
        self.after_month_var.set("1")
        self.after_day_var.set("1")
        self.topic_entry.delete(0, tk.END)
        self.filename_entry.delete(0, tk.END)

    def on_submit(self, event=None):
        Fetcher.peform(frame=self)