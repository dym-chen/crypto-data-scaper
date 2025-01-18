from playwright.sync_api import sync_playwright
import psycopg2 # connect python to postgres
from psycopg2.extras import execute_values # allows multiple rows to be inserted at once

def main():
    with sync_playwright() as p:

        # scarping the data

        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        page.goto('https://coinmarketcap.com/')
        page.wait_for_load_state('networkidle')  # Ensure the page has fully loaded

        # scrolling down page
        for i in range(5):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)

        trs_xpath = "//table[@class = 'sc-936354b2-3 tLXcG cmc-table']/tbody/tr"
        trs_list = page.query_selector_all(trs_xpath)

        data_list = []

        for coin in trs_list:
           coin_dict = {}   
           
           tds = coin.query_selector_all('//td')

           coin_dict['id'] = tds[1].inner_text()
           coin_dict['name'] = tds[2].query_selector("//p[contains(@class, 'coin-item-name')]").inner_text()
           coin_dict['symbol'] = tds[2].query_selector("//p[contains(@class, 'coin-item-symbol')]").inner_text()

           data_list.append(coin_dict)

        print(data_list)

        # save data into postgres

        browser.close()


if __name__ == '__main__':
    main()
