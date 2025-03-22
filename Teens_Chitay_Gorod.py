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
from Chitay_Gorod_Fantasy import create_driver, parse_books_Chitay_Gorod

url = 'https://www.chitai-gorod.ru/catalog/books/knigi-dlya-podrostkov-110132?page=1&filters%5BratingStars%5D=4&filters%5BratingStars%5D=5'

driver = create_driver(False)

driver.get(url)

prepared_books = parse_books_Chitay_Gorod(driver)

df_Chitay_Gorod_teens = pd.DataFrame(prepared_books, columns=['Book_Title', 'Author', 'Publisher', 'Age_Restriction', 'Rating', 'Price(in Rubles)'])

df_Chitay_Gorod_teens.to_csv('books_teens_Chitay_Gorod.csv', index=False)