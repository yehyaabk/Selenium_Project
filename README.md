# Booking Bot

Project created by **ABOU KHECHFE Yehya**

## Introduction

This project is a bot that navigates [Booking.com](https://www.booking.com/) in an automated way. The goal is to generate and scrape data from the website using Selenium, in order to automatically retrieve information about available hotels based on search criteria defined by the user.

## How the bot works

The bot follows these steps automatically:

1. Opens the Booking.com homepage
2. Handles and dismisses the cookie banner
3. Closes the sign-in popup that appears when the site loads
4. Selects the desired currency
5. Selects the destination
6. Selects the stay dates (check-in date and check-out date)
7. Selects the number of guests and the number of rooms
8. Launches the search, with or without the "traveling with pets" option
9. Closes the map that appears on the results page
10. Applies filters to the results (free cancellation, star rating)
11. Sorts the results from the lowest price to the highest
12. Retrieves the filtered data: hotel name, address, room type, score, number of reviews, and price

Here is the code corresponding to the full execution of the search flow:

```python
# Run the full booking search flow: open site, dismiss popups, configure search, apply filters, scrape results
bot.land_first_page()
bot.manage_cookies()
bot.dismiss_sign_in_popup()
bot.select_currency(currency=currency)
bot.select_destination(place_to_go=place_to_go)
bot.select_dates(check_in_date,check_out_date)
bot.select_guests_rooms(adults= adults,rooms=rooms) # you can add children number
# bot.
bot.go_to_search(traveling_with_pet)
bot.close_map()
# bot.filter_by_stars(*stars)
bot.free_cancellation() # if you only free cancellation  hotels
bot.sort_lowest_to_highest_price()
bot.get_filtered_hotels()
```

## Customization

The bot is  customizable. You can define your own search criteria by simply modifying the input parameters, without touching the bot's code itself. You can set:

- The desired currency
- The destination
- The check-in date and the check-out date
- The number of rooms
- The number of adult travelers
- The number of children as well as their age
- Filtering by hotel star rating
- Whether or not you are traveling with a pet

Here is an example of customizable parameters:

```python
#Search parameters / user inputs
currency = 'TRY'
place_to_go = 'Istanbul'
check_in_date = "2026-06-27"
check_out_date = "2026-08-20"
adults = 2
rooms = 1
traveling_with_pet = True
# if you want to filter by star rating
# stars=(2, 3, 4)
```

## Video demonstration

A demo video showing the bot's automated navigation on Booking.com is available below.

[Watch the demo video](https://www.youtube.com/watch?v=xAyPa0SfBLI)

## Results

Once the execution is complete, the collected data is saved in two formats:

- A **JSON** file, easily usable by other programs or scripts
- A **text file in table format**, directly readable by a human

This dual saving method allows the data collection process to be fully automated, while still keeping the ability to quickly review the results in a clear and organized way.

## Technologies used

- Python
- Selenium
- Tabulate

## Requirements

- Python 3 installed
- Google Chrome installed
- Project dependencies installed via pip

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Modify the search parameters in the execution file, then run the main script:

```bash
cd Booking_Bot
python run.py
```
