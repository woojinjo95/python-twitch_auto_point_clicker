import time
from threading import Event
from urllib.parse import unquote

from selenium.webdriver import Chrome, ChromeOptions

from config import user_path
from scripts.seleniumdriver import chromedriver_path, update_chrome
from scripts.simple_logger import simple_logger


logger = simple_logger()

update_chrome()
options = ChromeOptions()
options.add_argument(f'--user-data-dir={user_path}')

try:
    driver = Chrome(executable_path=chromedriver_path, options=options)
    driver.get('https://www.twitch.tv')

    event = Event()
    channel_name = None

    time.sleep(10)
    while True:
        url = driver.current_url
        if 'www.twitch.tv' in url and 'channel=' in url:
            if unquote(url.split('channel=')[1]) != channel_name:
                channel_name = unquote(url.split('channel=')[1])
                logger.info(f'Change channel to {channel_name}')
            buttons = driver.find_elements_by_css_selector('[aria-label="보너스 받기"]')
            if len(buttons) > 0:
                point = driver.find_elements_by_css_selector('[data-test-selector="balance-string"]')
                logger.info(f'{channel_name}: get point, Current: {point[0].text}')
                buttons[0].click()
                event.wait(2)
            else:
                event.wait(10)

        else:
            event.wait(10)

finally:
    driver.close()
