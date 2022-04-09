import os
from threading import Event

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver import Chrome, ChromeOptions

from config import user_path
from scripts.seleniumdriver import chromedriver_path, update_chrome
from scripts.simple_logger import simple_logger
from scripts.twtich import change_to_twitch_window, get_channel_name, get_point

logger = simple_logger()
update_chrome()
os.makedirs(user_path, exist_ok=True)


def main():
    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={user_path}')

    driver = None
    try:
        driver = Chrome(executable_path=chromedriver_path, options=options)
        driver.get('https://www.twitch.tv')
        event = Event()
        channel_info = {'name': ''}
        while True:
            change_to_twitch_window(driver, channel_info)
            get_channel_name(logger, driver, channel_info)
            get_point(logger, driver, channel_info)
            event.wait(5)

    except InvalidArgumentException:
        logger.error(f'{user_path} is used by other chrome')

    finally:
        if driver:
            driver.close()


if __name__ == '__main__':
    main()
