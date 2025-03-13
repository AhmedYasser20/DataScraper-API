from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import random
from flask import Flask, send_file, request


app = Flask(__name__)


def scrape_google_maps(search_keyword, max_businesses):
    
    driver = webdriver.Chrome()

    
    driver.get("https://www.google.com/maps")

    # Allow the page to load
    time.sleep(5)

    # Search for businesses
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(search_keyword)
    search_box.send_keys(Keys.ENTER)

    # Allow search results to load
    time.sleep(5)


    businesses = []
    business_count = 0

    while business_count < max_businesses:
        business_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK")

        for i in range(len(business_elements)):
            if business_count >= max_businesses:
                break

            business = business_elements[i]

            try:
                name = business.find_element(By.CLASS_NAME, "qBF1Pd").text
            except:
                name = "N/A"
            
            try:
                address = business.find_element(By.CLASS_NAME, "lI9IFe").text
            except:
                address = "N/A"

            # Click on the business to get more details
            business.click()
            time.sleep(3)  

            try:
                phone = driver.find_element(By.XPATH, "//button[contains(@data-tooltip, 'Copy phone number')]").text
            except:
                phone = "N/A"
            try:
                website = driver.find_element(By.XPATH, "//a[contains(@data-tooltip, 'Open website')]").get_attribute("href")
            except:
                website = "N/A"
            try:
                reviews = driver.find_element(By.CLASS_NAME, "UY7F9").text
            except:
                reviews = "N/A"
            try:
                rating = driver.find_element(By.CLASS_NAME, "MW4etd").text
            except:
                rating = "N/A"

            businesses.append({
                "Name": name,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Reviews": reviews,
                "Rating": rating
            })

            business_count += 1

            
            driver.back()
            time.sleep(3)  

            # Re-fetch the list of business elements
            business_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK")

        # Check if there is a next page and we still need more businesses
        if business_count < max_businesses:
            try:
                scrollable_div = driver.find_element(By.CSS_SELECTOR, "[role='feed']")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(random.randint(2, 5)) 
            except:
                break

    
    df = pd.DataFrame(businesses)
    df.to_csv("businesses.csv", index=False)

    
    driver.quit()

@app.route('/download_csv')
def download_csv():
    search_keyword = request.args.get('search_keyword', default='Marketing Agencies in Dubai', type=str)
    max_businesses = request.args.get('max_businesses', default=20, type=int)
    scrape_google_maps(search_keyword, max_businesses)
    return send_file("businesses.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)