import time, os
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd

def scroll(driver):
    y = 1000
    for i in range(0, 8):
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 1000  
        time.sleep(1.5)

def scrape_list_of_products(driver, link):
    time.sleep(5)
    driver.get(link)
    scroll(driver)
    links = [link.get_attribute("href") for link in driver.find_elements(By.CLASS_NAME, 'pcv3__info-content.css-gwkf0u')]
    return links

def scrape_product(driver, links):
    names, descriptions, image_links, prices, ratings, merchants = [], [], [], [], [], []
    for link in links:
        if 'ta.tokopedia.com' not in link:
            driver.get(link)
            time.sleep(5)
            name = driver.find_element(By.XPATH, "//*[@data-testid='lblPDPDetailProductName']").text
            desc = driver.find_element(By.XPATH, "//*[@data-testid='lblPDPDescriptionProduk']").text
            image_link = driver.find_element(By.XPATH, "//*[@data-testid='PDPMainImage']").get_attribute('src')
            price = driver.find_element(By.XPATH, "//*[@data-testid='lblPDPDetailProductPrice']").text.replace('Rp', '').replace('.', '')
            rating = driver.find_element(By.XPATH, "//*[@data-testid='lblPDPDetailProductRatingNumber']").text
            merchant = driver.find_element(By.XPATH, "//*[@data-testid='llbPDPFooterShopName']").find_element(By.TAG_NAME, "h2").text
            names.append(name)
            descriptions.append(desc)
            image_links.append(image_link)
            prices.append(price)
            ratings.append(rating)
            merchants.append(merchant)
    driver.close()
    return names, descriptions, image_links, prices, ratings, merchants

link = 'https://www.tokopedia.com/search?navsource=&ob=8&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q=handphone'
options = Options()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
edge_driver_binary = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"
driver = webdriver.Edge(edge_driver_binary, options = options)
links = scrape_list_of_products(driver, link)
names, descriptions, image_links, prices, ratings, merchants = scrape_product(driver, links)
datas = {'names': names, 'image_links': image_links, 'prices': prices, 'ratings': ratings, 'merchants': merchants}
dataframe = pd.DataFrame(data=datas)
dataframe.to_csv('data_handphone_tokopedia.csv', index=False, sep=';')
print(dataframe)