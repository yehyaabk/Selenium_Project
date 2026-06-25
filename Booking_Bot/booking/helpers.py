from datetime import datetime,timedelta
from typing import List
from tabulate import tabulate
import json

def verify_dates(checkin, checkout):

    current_date= datetime.now().strftime("%Y-%m-%d")
    max_selectable_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")

    if checkout < checkin :
        checkin, checkout = checkout, checkin

    if checkin < current_date :
        checkin = current_date

    if checkout > max_selectable_date:
        checkout = max_selectable_date

    return checkin, checkout

def get_months_between(date1, date2):
    year1 = datetime.strptime(date1, "%Y-%m-%d").year
    year2 = datetime.strptime(date2, "%Y-%m-%d").year
    month1= datetime.strptime(date1, "%Y-%m-%d").month
    month2 = datetime.strptime(date2, "%Y-%m-%d").month

    if year1 == year2 :
        return month2 - month1
    else:
        return (12-month1) + month2

def save_as_table(data:List[dict]):
    table = tabulate(data, headers='keys', tablefmt="fancy_grid")
    with open("output/hotels.txt", "w", encoding='utf-8') as file:
        file.write(table)

    print("Scraped Data Are Saved As a Table")


def save_as_json(data:List[dict]):
    with open("output/hotels.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print("Scraped Data Are Saved As Json file")










