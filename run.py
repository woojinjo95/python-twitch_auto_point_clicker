import os
import time

from selenium.webdriver import Chrome, ChromeOptions
from seleniumdriver import update_chrome
from threading import Event
from urllib.parse import unquote

user_path = r"C:\Users\SHF\AppData\Local\Google\Chrome\User Data"
update_chrome()
options = ChromeOptions()
options.add_argument(f'--user-data-dir={user_path}')

try:
    driver = Chrome(os.path.join('Chromedriver', 'chromedriver.exe'), options=options)
    driver.get('https://www.twitch.tv')

    event = Event()

    time.sleep(10)
    while True:
        url = driver.current_url
        if 'www.twitch.tv' in url and 'channel=' in url:
            channel_name = unquote(url.split('channel=')[1])
            buttons = driver.find_elements_by_css_selector('[aria-label="보너스 받기"]')
            if len(buttons) > 0:
                point = driver.find_elements_by_css_selector('[data-test-selector="balance-string"]')
                print(f'{channel_name}: get point, Current: {point[0].text}')
                buttons[0].click()
                event.wait(5)
            else:
                event.wait(30)
            
        else:
            event.wait(30)

finally:
    driver.close()
