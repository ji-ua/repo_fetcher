import os
from tkinter import messagebox
import requests
import json


class Fetcher():
  @classmethod
  def peform(self, frame):
     self.set_condition(frame=frame)
     query = self.construct_query()
     data = self.fetch_data(query=query)
     self.save_data_with_selection(data=data)

  @classmethod
  def set_condition(self, frame):
    self.forks_min = frame.forks_min_entry.get()
    self.forks_max = frame.forks_max_entry.get()
    self.pushed_before = self.set_date(year=frame.before_year_var.get(), month=frame.before_month_var.get(), day=frame.before_day_var.get())
    self.pushed_after = self.set_date(year=frame.after_year_var.get(), month=frame.after_month_var.get(), day=frame.after_day_var.get())
    self.topic = frame.topic_entry.get()
    self.archived = frame.archived_var.get()
    self.format = frame.format_var.get()
    self.filename = frame.filename_entry.get()
  
  @classmethod
  def construct_query(self):
    query_parts = [f"archived:{self.archived}", f"topic:{self.topic}"]

    # フォーク数の条件を追加
    if self.forks_min and self.forks_max:
        query_parts.append(f"forks:{self.forks_min}..{self.forks_max}")
    elif self.forks_min:
        query_parts.append(f"forks:>={self.forks_min}")
    elif self.forks_max:
        query_parts.append(f"forks:<={self.forks_max}")

    # プッシュ日時の条件を追加
    if self.pushed_before:
        query_parts.append(f"pushed:<{self.pushed_before}")
    if self.pushed_after:
        query_parts.append(f"pushed:>{self.pushed_after}")

    query = " ".join(query_parts)

    return f"""
    {{
      search(query: "{query}", type: REPOSITORY, first: 100) {{
        edges {{
          node {{
            ... on Repository {{
              nameWithOwner
              url
              pushedAt
              forks {{
                totalCount
              }}
            }}
          }}
        }}
      }}
    }}
    """
  
  def set_date(year, month, day):
     if year and month and day:
        return f"{year}-{int(month):02d}-{int(day):02d}"
     return ''
  
  @classmethod
  def fetch_data(self, query):
    token = os.getenv('GITHUB_API_KEY')
    
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)


    return response
  
  @classmethod
  def save_data_with_selection(self, data):
    selections = {
        "selections": {
           "forks_min": self.forks_min,
           "forks_max": self.forks_max,
           "pushed_before": self.pushed_before,
           "pushed_after": self.pushed_after,
           "topic": self.topic,
           "archived": self.archived,
           "format": self.format,
           "filename": self.filename
        }
    }

    combined_data = {
      "condition": selections,
      "feature": data.json()
    }

    filename_with_extension = f"{self.filename}.{self.format.lower()}"

    if not os.path.isfile(filename_with_extension):
      if self.format == "json":
        with open(f"{filename_with_extension}", "w") as file:
          json.dump(combined_data, file, indent=4)

        messagebox.showinfo("success", f"save {filename_with_extension} .")
    else:
      messagebox.showwarning("warning", f"{filename_with_extension} already exists.")