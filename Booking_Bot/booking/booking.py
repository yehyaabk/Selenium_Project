from selenium import  webdriver
from selenium.webdriver.common.by import  By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from . import constants  as const
from . import helpers
from.helpers import save_as_json, save_as_table
from .booking_report import get_hotels_container, get_hotel_cards, extract_hotels_data, scroll_to_load_all_hotels
import time

class Booking(webdriver.Chrome):
    def __init__(self, auto_close=False, accept_cookies=False):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        self.auto_close = auto_close
        self.accept_cookies= accept_cookies
        super().__init__(options=options)
        self.maximize_window()
        self.implicitly_wait(5)

    def land_first_page(self):
        self.get(const.BASE_URL)
    def manage_cookies(self):
        try:
            if self.accept_cookies:
                accept_button = self.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_button.click()
                time.sleep(const.DURATION)
            else:
                decline_button = self.find_element(By.ID, "onetrust-reject-all-handler")
                decline_button.click()
                time.sleep(const.DURATION)
        except  TimeoutException :
            print("No cookie banner found")


    def dismiss_sign_in_popup(self):
        try:
            button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
            button.click()
            time.sleep(const.DURATION)
        except TimeoutException:
            print("No sign-in popup found")

    def select_currency(self,  currency='USD'):
        currencies_trigger = self.find_element(By.CSS_SELECTOR,"button[aria-haspopup='dialog'][data-testid='header-currency-picker-trigger']")
        currencies_trigger.click()
        time.sleep(const.DURATION)

        xpath=f"//div[contains(text(), '{currency}')]/ancestor::button[1]"
        currency_button = self.find_element(By.XPATH,xpath)
        currency_button.click()

    def select_destination(self, place_to_go='paris'):
        destination_input = self.find_element(By.CSS_SELECTOR,'input[placeholder="Where are you going?"][data-destination="1"]')
        destination_input.clear()
        destination_input.send_keys(place_to_go)

        wait = WebDriverWait(self, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, "autocomplete-result-1"), place_to_go))

        first_choice = self.find_element(By.ID, "autocomplete-result-1")
        first_choice.click()
        time.sleep(const.DURATION)

    def select_dates(self, check_in_date, check_out_date):
        check_in_date, check_out_date = helpers.verify_dates(check_in_date, check_out_date)
        months_between_checkin_checkout = helpers.get_months_between(check_in_date, check_out_date)
        current_date = datetime.now().strftime("%Y-%m-%d")
        months_between_current_checkin = helpers.get_months_between(current_date, check_in_date)

        for _ in range(months_between_current_checkin):
            next_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Next month"]')
            next_button.click()
            time.sleep(const.DURATION)

        checkin_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        checkin_element.click()
        time.sleep(const.DURATION)

        for _ in range(months_between_checkin_checkout):
            next_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Next month"]')
            next_button.click()
            time.sleep(const.DURATION)

        checkout_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        checkout_element.click()
        ActionChains(self).move_by_offset(10, 10).click().perform()

    def select_guests_rooms(self,adults=2, children=0, rooms=1):
        occupancy_field = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        occupancy_field.click()
        # wait = WebDriverWait(self, 10)
        # wait.until(EC.visibility_of_element_located((By.ID, "group_adults")))

        time.sleep(const.DURATION)
        self.select_adults(adults)
        self.select_children(children)
        self.select_rooms(rooms)

    def select_adults(self,adults):
        parent_div = self.find_element(By.XPATH, "//input[@id='group_adults']/preceding-sibling::div[1]")
        # print(parent_div.get_attribute("outerHTML"))
        span_element  = parent_div.find_element(By.CSS_SELECTOR, 'span.e32aa465fd[aria-hidden="true"]')
        default_num = int(span_element.text)
        # print(default_num)
        clicks_num = adults - default_num

        if clicks_num >=0:
            for _ in range (clicks_num):
                increase_button = parent_div.find_element(By.XPATH, "./button[2]")
                increase_button.click()
                time.sleep(const.DURATION)
        else:
            for _ in range(-1 * clicks_num):
                decrease_button = parent_div.find_element(By.XPATH, "./button[1]")
                decrease_button.click()
                time.sleep(const.DURATION)


    def select_children(self,children):
        div_element = self.find_element(By.XPATH, "//input[@id='group_children']/preceding-sibling::div[1]")
        for _ in range(children):
            increase_button = div_element.find_element(By.XPATH, "./button[2]")
            increase_button.click()
            time.sleep(const.DURATION)

    def select_rooms(self, rooms):
        parent_div = self.find_element(By.XPATH, "//input[@id='no_rooms']/preceding-sibling::div[1]")
        # span_element = parent_div.find_element(By.CSS_SELECTOR, 'span.e32aa465fd[aria-hidden="true"]')
        # default_num = int(span_element.text)
        # print(default_num)
        for _ in range(rooms - 1):
            increase_button = parent_div.find_element(By.XPATH, "./button[2]")
            increase_button.click()
            time.sleep(const.DURATION)

    def set_children_ages(self, *ages):
        for index, age in enumerate(ages):
            parent_div = self.find_element(By.CSS_SELECTOR, 'div[data-testid="kids-ages"]')
            child_divs = parent_div.find_elements(By.CSS_SELECTOR, 'div[data-testid="kids-ages-select"]')

            dropdown = Select(child_divs[index].find_element(By.CSS_SELECTOR, "select"))
            dropdown.select_by_value(str(age))
            time.sleep(0.5)  # give React time to finish re-rendering before next iteration!

    def go_to_search(self, traveling_with_pet=False, add_flights=False , entire_home=False, traveling_for_work=False ):
        if traveling_with_pet:
            parent_label = self.find_element(By.CSS_SELECTOR, "label[for='pets']")
            # print(parent_label.get_attribute("outerHTML"))
            span =  parent_label.find_element(By.TAG_NAME, "span")
            span.click()
            time.sleep(const.DURATION)
        done_button = self.find_element(By.XPATH,"//span[contains(text(),'Done')]/parent::button")
        # print(done_button.get_attribute("outerHTML"))
        done_button.click()
        if add_flights:
            add_flights= self.find_element(By.CSS_SELECTOR, 'input[name="sb_flight_search"][value="flight"]')
            add_flights.click()
        if traveling_for_work:
            try:
                check_work = self.find_element(By.CSS_SELECTOR, 'input[name="sb_travel_purpose"][value="business"]')
                check_work.click()
            except:
                print("Not Found!!!!")
        form = self.find_element(By.CSS_SELECTOR, r'form[action="https://www.booking.com/searchresults.html"]')
        buttons = form.find_elements(By.TAG_NAME, "button")
        search_button = buttons[-1]
        search_button.click()

    def filter_by_stars(self, *stars):
        parent_div = self.find_element(By.CSS_SELECTOR,'div[id*="filter_group_class"][data-testid="filters-group-container"]')
        star_divs = parent_div.find_elements(By.XPATH, "./*")
        # self.execute_script("arguments[0].scrollIntoView(true);", parent_div)
        # time.sleep(0.5)
        for star in stars:
            star_divs[star - 2].click()

        # self.execute_script("window.scrollTo(0, 0);")


    def sort_lowest_to_highest_price(self):
        dropdown_button = self.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        ActionChains(self).move_to_element(dropdown_button).perform()
        dropdown_button.click()

        time.sleep(const.DURATION)

        lowest_price = self.find_element(By.CSS_SELECTOR, 'button[data-id="price"][aria-label="Price (lowest first)"]')
        # ActionChains(self).move_to_element(lowest_price).perform()
        # time.sleep(2)
        lowest_price.click()


    def close_map(self):
        try:
            close_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Close map"]')
            # print(close_button.get_attribute("outerHTML"))
            close_button.click()
        except NoSuchElementException:
            print("No Map")

    def  free_cancellation(self):
        try :
            free_cancellation_div = self.find_element(By.XPATH,'.//div[contains(text(), "Free cancellation")]')
            self.execute_script("arguments[0].scrollIntoView(true);", free_cancellation_div)
            time.sleep(0.5)

            free_cancellation_div.click()
            time.sleep(0.5)

            self.execute_script("window.scrollTo(0,0);")

        except NoSuchElementException:
            print("Element Not Found")
        except StaleElementReferenceException:
            print("Stale Element Reference Exception")
        except Exception:
            raise  ValueError("Bahh An error !!")


    def get_filtered_hotels(self):
        scroll_to_load_all_hotels(self)
        hotels_container = get_hotels_container(self)
        hotel_cards = get_hotel_cards( hotels_container= hotels_container )
        # print(type(hotel_cards))
        print(len(hotel_cards))
        hotels_data = extract_hotels_data(hotel_cards = hotel_cards)
        # print(hotels_data)
        save_as_json(hotels_data)
        save_as_table(hotels_data)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_close:
            self.quit()


