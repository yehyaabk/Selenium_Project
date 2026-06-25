from subprocess import check_output

import booking.constants as const
from booking.booking import Booking
from selenium.common.exceptions import TimeoutException


with Booking() as bot:
    #Search parameters / user inputs
    currency = 'USD'
    place_to_go = 'Paris'
    check_in_date = "2026-06-27"
    check_out_date = "2026-08-20"
    adults = 4
    rooms = 2
    traveling_with_pet = True
    # if you want to filter by star rating
    # stars=(2, 3, 4)

    # Run the full booking search flow: open site, dismiss popups, configure search, apply filters, scrape results
    bot.land_first_page()
    bot.manage_cookies()
    bot.dismiss_sign_in_popup()
    bot.select_currency(currency=currency)
    bot.select_destination(place_to_go=place_to_go)
    bot.select_dates(check_in_date,check_out_date)
    bot.select_guests_rooms(adults= adults,rooms=rooms) # you can add children age
    # bot.set_children_ages(1,3,5)
    bot.go_to_search(traveling_with_pet)
    bot.close_map()
    # bot.filter_by_stars(*stars)
    # bot.free_cancellation() # if you only free cancellation  hotels
    bot.sort_lowest_to_highest_price()
    bot.get_filtered_hotels()








