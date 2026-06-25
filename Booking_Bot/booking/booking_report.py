# Helper functions for retrieving and displaying hotel data
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import List
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from typing import Optional, Union, Tuple
import re
import time

# to prevent lazy loading !
def scroll_to_load_all_hotels(driver: WebDriver, pause_time=1, max_scrolls=20):
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # no MORE new content loaded, STOP scrolling
        last_height = new_height

def get_hotels_container(driver:WebDriver)  :
    try:
        hotels_container = driver.find_element(By.CSS_SELECTOR, 'div[role="list"][data-results-container="1"]')
        # print(hotels_container)
        return hotels_container
    except NoSuchElementException:
        raise ValueError("No Such Element Exception in get_hotels_container() function")
    except StaleElementReferenceException:
        raise ValueError("Stale Element Reference Exception in get_hotels_container() function")
    except Exception:
        raise ValueError("An Exception in get_hotels_container() function ")


def get_hotel_cards(hotels_container:WebElement)  -> List[WebElement]:
    try:
           hotel_cards = hotels_container.find_elements(By.CSS_SELECTOR,'div[data-testid="property-card"][role="listitem"]')
           return  hotel_cards

    except Exception:
        raise ValueError("An Exception  Error in get_hotel_cards() function")




def extract_hotels_data(hotel_cards:List[WebElement]) -> List[dict]:
    try:
        hotels_data = []
        for hotel_card in hotel_cards:
            temp_dic = {}

            # find title
            title = hotel_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute("innerHTML")
            # find score
            try:
                parent_score_div = hotel_card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]')
                score_div = parent_score_div.find_element(By.XPATH, "./div[2]")
                score = score_div.text
            except NoSuchElementException:
                score = "No score yet"

            try:
                parent_score_div = hotel_card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]')
                review_div_1 = parent_score_div.find_element(By.XPATH, "./div[3]")
                review_div_2 = review_div_1.find_element(By.XPATH, "./div[2]")
                review = review_div_2.text
                review_number = get_number(text= review)
            except  NoSuchElementException:
                review_number= 0
            hotel_address = get_address(hotel_card)
            currency, price = get_hotel_price_and_currency(hotel_card)
            hotel_type = get_hotel_type(hotel_card = hotel_card)

            temp_dic["Name"]=title
            temp_dic["Address"] = hotel_address
            temp_dic["type"] =  hotel_type
            temp_dic["Score"] = score
            temp_dic["Review Number"] = review_number
            temp_dic[f"Price ({currency})"] = price

            hotels_data.append(temp_dic)
        return hotels_data
    except Exception:
        raise

def get_address(hotel_card:WebElement) -> str:
    try :
        address_link = hotel_card.find_element(By.CSS_SELECTOR, 'span[data-testid="address-link"]')
        hotel_address = address_link.get_attribute("innerHTML")
        return  hotel_address
    except NoSuchElementException:
        return "No Address"

def get_hotel_price_and_currency(hotel_card:WebElement) -> Tuple[Optional[str],Optional[float]]:
    try:
        price_span = hotel_card.find_element(By.XPATH, ".//span[@data-testid='price-and-discounted-price']")
        currency, price = get_price_and_currency(price_span.text)
        return currency, price
    except NoSuchElementException:
        return None, None

def get_price_and_currency(text: str) -> Tuple[Optional[str],Optional[float]]:
    cleaned_text = text.replace(",", '')

    reg_pattern = r"([^\d\s]+)\s*([\d\.]+)"

    match = re.match(reg_pattern, cleaned_text)

    if match:
        currency = match.group(1)
        price = float(match.group(2))
        return currency, price
    return None , None


def get_hotel_type(hotel_card:WebElement ) -> str :
    try:
        parent_div = hotel_card.find_element(By.XPATH, './/div[@data-testid="recommended-units"]')
        hotel_type = parent_div.find_element(By.CSS_SELECTOR, "h4").text
        return hotel_type
    except NoSuchElementException:
        return "Not Mentioned"


def get_number(text: str) -> Optional[Union[int, float]]:
    """Extract the first number from a string, handling commas as thousand separators."""
    cleaned_text = text.replace(",", "")
    match = re.search(r'\d+\.?\d*', cleaned_text)

    if match:
        number_str = match.group()
        if '.' in number_str:
            return float(number_str)  # has a decimal point → float
        else:
            return int(number_str)  # no decimal point → int
    return None



