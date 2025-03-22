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

def parse_books_Labirint(driver_):
    book_links = []
    book_prices = []
    book_names = []
    book_authors = []
    book_publishers = []
    book_ratings = []

    try:
        books = WebDriverWait(driver_, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-title="Все в жанре «Книги для детей»"]')))

        book_descriptions = books.find_elements(By.CSS_SELECTOR, 'div[class="genres-carousel__item"]')

        book_price = books.find_elements(By.CSS_SELECTOR, 'div[class="price-label"]')

        book_publisher = books.find_elements(By.CSS_SELECTOR, 'a[class="product-pubhouse__pubhouse"]')

        for book in book_descriptions:
            book_info = book.find_element(By.CSS_SELECTOR, 'a[class="product-title-link"]')

            book_links.append(book_info.get_attribute('href'))

            book_authors.append(book_info.get_attribute('title').split('-')[0])

            if len(book_info.get_attribute('title').split('-')) == 2:
                book_names.append(book_info.get_attribute('title').split('-')[1])
            else:
                book_names.append(book_info.find_element(By.CSS_SELECTOR, 'span').text)

        for price in book_price:
            price_of_the_book = price.find_element(By.CSS_SELECTOR, 'span').text
            book_prices.append(int(''.join([letter for letter in price_of_the_book if letter.isdigit()])))

        for publish in book_publisher:
            book_publishers.append(publish.get_attribute('title'))

        for link in book_links:
            try:
                driver.get(link)

                try:
                    rating = driver.find_element(By.CSS_SELECTOR, 'div[class="_rating_zg87a_1 text-med-16 cursor-pointer"]')
                    book_ratings.append(rating.find_element(By.CSS_SELECTOR, 'span ').text)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
        return(list(zip(book_names, book_authors, book_publishers, book_ratings, book_prices)))

    except Exception as e:
        print(e)
    finally:
        driver_.quit()

try:
    url = 'https://www.labirint.ru/genres/1850/?order=popularity&way=forward'
    driver = create_driver(False)
    driver.get(url)
    parsed_books = parse_books_Labirint(driver)
    df_kids_lab = pd.DataFrame(parsed_books, columns=['Book_Title', 'Author', 'Book_Publisher', 'Rating', 'Price'])
    df_kids_lab.to_csv('books_kids_lab.csv', index=False)
except Exception as e:
    print(e)