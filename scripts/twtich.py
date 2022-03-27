from calendar import c
import logging
import traceback
import re
from urllib.parse import unquote

from selenium.webdriver import ActionChains

logger = logging.getLogger('main')


def get_exact_point(driver):
    try:
        target = driver.find_element_by_css_selector('[data-test-selector="balance-string"]')
        mouse_action = ActionChains(driver)
        mouse_action.move_to_element(target)
        mouse_action.perform()

        name_list = ['추억', '채널']
        candidate_list = []
        for name in name_list:
            candidate_list += driver.find_elements_by_xpath(f"//*[contains(text(), '{name} 포인트')]")

        if len(candidate_list) > 0:
            text_with_point = candidate_list[0].text
            text_with_only_point = re.search(r'\d{1,3}(,\d{3})*', text_with_point).group()
            point = int(text_with_only_point.replace(',', ''))
        else:
            point = None
        return point

    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None


def get_point(logger, driver, channel_info: dict):
    try:
        url = driver.current_url
        if 'www.twitch.tv' in url and 'channel=' in url:
            buttons = driver.find_elements_by_css_selector('[aria-label="보너스 받기"]')
            channel_name = channel_info.get('name')

            while len(buttons) > 0:
                point_prev = get_exact_point(driver)
                buttons[0].click()
                point = get_exact_point(driver)
                logger.info(f'{channel_name}: get point, {point_prev}=>{point}')

    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None


def get_channel_name(logger, driver, channel_info):
    try:
        url = driver.current_url
        channel_name = unquote(url.split('channel=')[1])
        if channel_name != channel_info.get('name'):
            channel_info['name'] = channel_name
            point = get_exact_point(driver)
            logger.info(f'Change channel to {channel_name}, point: {point}')
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None
