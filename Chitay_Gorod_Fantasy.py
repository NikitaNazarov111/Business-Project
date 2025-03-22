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
import numpy as np

def create_driver(headless=True):

    options = uc.ChromeOptions()
    options.headless = headless
    return uc.Chrome(options=options)

def parse_books_Chitay_Gorod(driver_):
    book_links = []
    book_prices = []
    book_ages = []
    book_names = []
    book_authors = []
    book_publishers = []
    book_ratings = []

    try:
        books_description = WebDriverWait(driver_, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card__text.product-card__row')))[:48]

        book_author = WebDriverWait(driver_, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-title__author')))[:48]

        book_price = WebDriverWait(driver_, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-price__value.product-price__value--discount')))[:48]

        for description in books_description:
            try:
                link = description.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                book_links.append(link)
                print(link)
            except Exception as e:
                book_links.append(np.nan)

            try:
                book_name = description.find_element(By.CSS_SELECTOR, 'a').get_attribute('title')
                book_names.append(book_name)
                print(book_name)
            except Exception as e:
                book_names.append(np.nan)

        for author in book_author:
            try:
                book_authors.append(author.text)
            except Exception as e:
                book_authors.append(np.nan)

        for price in book_price:
            try:
                price = int(''.join([letter for letter in price.text if letter.isdigit()]))
                book_prices.append(price)
            except Exception as e:
                book_prices.append(np.nan)

        for link in book_links:
            try:
                driver.get(link)

                try:
                    rating = driver.find_element(By.CSS_SELECTOR, 'span.product-review-range__count').text
                    book_ratings.append(rating)
                except Exception as e:
                    book_ratings.append(np.nan)

                try:
                    publisher = driver.find_element(By.CSS_SELECTOR, 'a[itemprop="publisher"]').get_attribute('content')
                    book_publishers.append(publisher)
                except Exception as e:
                    book_publishers.append(np.nan)

                try:
                    age = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="typicalAgeRange"]').text
                    book_ages.append(age)
                except Exception as e:
                    book_ages.append(np.nan)

            except Exception as e:
                book_ratings.append(np.nan)
                book_publishers.append(np.nan)
                book_ages.append(np.nan)

    except Exception as e:
        print(f"Произошла глобальная ошибка: {e}")

    return list(zip(book_names, book_authors, book_publishers, book_ages, book_ratings, book_prices))

url = 'https://www.chitai-gorod.ru/catalog/books/fantastika-fehntezi-110004?page=1&filters%5BratingStars%5D=4&filters%5BratingStars%5D=5'

driver = create_driver(False)

driver.get(url)

prepared_books = parse_books_Chitay_Gorod(driver)

df_Chitay_Gorod_Fantasy = pd.DataFrame(prepared_books, columns=['Book_Title', 'Author', 'Publisher', 'Age_Restriction', 'Rating', 'Price(in Rubles)'])

df_Chitay_Gorod_Fantasy.to_csv('books_Fantasy_Chitay_Gorod.csv', index=False)


