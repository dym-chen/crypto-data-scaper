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

        page.wait_for_timeout(5000)

        # save data into postgres

        browser.close()


if __name__ == '__main__':
    main()
