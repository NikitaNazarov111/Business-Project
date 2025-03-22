import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc

def create_driver(headless=True):

    options = uc.ChromeOptions()
    options.headless = headless
    return uc.Chrome(options=options)

def setup_website(driver_, url_, sort_value='3', items_per_page='2'):

    driver_.get(url_)

    wait = WebDriverWait(driver_, 10)
    sort_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.sorting-select.sort')))
    Select(sort_select).select_by_value(sort_value)

    items_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.sorting-select.onpage')))
    Select(items_select).select_by_value(items_per_page)

    return driver_

def parse_books_MDK(driver_):
    book_links = []
    book_prices = []
    book_genres = []
    book_names = []
    book_authors = []
    book_publishers = []

    book_genre = driver_.find_elements(By.CSS_SELECTOR, 'ul.tg-bookscategories')[:50]
    book_name = driver_.find_elements(By.CSS_SELECTOR, 'div.tg-booktitle')[:50]
    book_author = driver_.find_elements(By.CSS_SELECTOR, 'span.tg-bookwriter')[:50]
    book_price = driver_.find_elements(By.CSS_SELECTOR, 'span.tg-bookprice')[:50]

    for genre in book_genre:
        book_genres.append(genre.find_element(By.CSS_SELECTOR, 'a').text)
    for name in book_name:
        name_of_book = name.find_element(By.CSS_SELECTOR, 'a')
        book_names.append(name_of_book.text)
        book_links.append(name_of_book.get_attribute('href'))

    for author in book_author:
        book_authors.append(author.find_element(By.CSS_SELECTOR, 'a').text)

    for price in book_price:
        book_prices.append(int(price.find_element(By.CSS_SELECTOR, 'ins').text[:-1].strip()))

    for link in book_links:
        driver_.get(link)
        publisher = driver_.find_element(By.CSS_SELECTOR, 'meta[itemprop="publisher"]').get_attribute('content')
        book_publishers.append(publisher)
    return list(zip(book_names, book_genres, book_authors, book_publishers, book_prices))

try:
    driver = create_driver(False)
    url = 'https://mdk-arbat.ru/catalog/?subj_id=3217'
    driver = setup_website(driver, url)
    time.sleep(5)
    prepared_list = parse_books_MDK(driver)

    df_adults = pd.DataFrame(prepared_list, columns=['Book_Title', 'Book_Genre', 'Author', 'Publisher', 'Price(in Rubles)'])
    df_adults['Age_Category'] = 'Adult'
    df_adults.to_csv('books_ADULT_MDK.csv', index=False)

except Exception as e:
    print(f'Произошла ошибка: {e}')

finally:
    if driver and hasattr(driver, 'quit'):
        driver.quit()
