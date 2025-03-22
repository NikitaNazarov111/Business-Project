import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
from Adult_Fiction_MDK import create_driver
from Adult_Fiction_MDK import setup_website
from Adult_Fiction_MDK import parse_books_MDK

try:
    driver = create_driver(False)
    url = 'https://mdk-arbat.ru/catalog?subj_id=48'
    driver = setup_website(driver, url)
    time.sleep(5)
    prepared_list = parse_books_MDK(driver)

    df_kids = pd.DataFrame(prepared_list, columns=['Book_Title', 'Book_Genre', 'Author', 'Publisher', 'Price(in Rubles)'])
    df_kids['Age_Category'] = 'Kids'
    df_kids.to_csv('books_KIDS_MDK.csv', index=False)

except Exception as e:
    print(f'Произошла ошибка: {e}')

finally:
    if driver and hasattr(driver, 'quit'):
        driver.quit()
