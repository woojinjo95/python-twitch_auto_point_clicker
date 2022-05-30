import logging
import re
import sys
import time
import traceback
from urllib.parse import unquote

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

logger = logging.getLogger('main')


def get_exact_point(driver):
    point = None
    try:
        targets = driver.find_elements_by_css_selector('[data-test-selector="balance-string"]')
        if len(targets) > 0:
            target = targets[0]
            mouse_action = ActionChains(driver)
            mouse_action.move_to_element(target)
            mouse_action.perform()
            driver.implicitly_wait(1)
            time.sleep(1)

            name_list = ['추억', '채널']
            candidate_list = []
            for name in name_list:
                point_text = driver.find_elements_by_xpath(f"//*[contains(text(), '{name} 포인트')]")
                candidate_list += point_text

            if len(candidate_list) > 0:
                text_with_point = candidate_list[0].text
                text_with_only_point = re.search(r'\d{1,3}(,\d{3})*', text_with_point).group()
                point = int(text_with_only_point.replace(',', ''))

        return point
    except WebDriverException:
        logger.warn('Chrome closed.')
        sys.exit()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None


def get_point(logger, driver, channel_info: dict):
    try:
        url = driver.current_url
        if 'twitch.tv' in url:
            buttons = driver.find_elements_by_css_selector('[aria-label="보너스 받기"]')
            if len(buttons) == 0:
                return
            channel_name = channel_info.get('name')

            if len(buttons) > 0:
                point_prev = get_exact_point(driver)
                buttons[0].click()
                point = get_exact_point(driver)
                logger.info(f'{channel_name}: get point, {point_prev}=>{point}')
                time.sleep(1)

    except WebDriverException:
        logger.warn('Chrome closed.')
        sys.exit()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None


def get_channel_name(logger, driver, channel_info):
    try:
        channel_string = driver.current_url.split('/')[2:]
        if len(channel_string) < 2:
            logger.debug('Fail to find channel name')
        else:
            if '?' in channel_string:
                channel_name = unquote(channel_string[-1])
            else:
                channel_name = channel_string[1]
            if channel_name != channel_info.get('name'):
                channel_info['name'] = channel_name
                point = get_exact_point(driver)
                logger.info(f'Change channel to {channel_name}, point: {point}')
            else:
                # same channel
                pass
    except WebDriverException:
        logger.warn('Chrome closed.')
        sys.exit()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return None


def change_to_twitch_window(driver, channel_info):
    try:
        channel_url = driver.current_url
        if 'twitch' not in channel_url and channel_url != channel_info['channel_url']:
            logger.info('Current page is not twitch!')
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)
                if 'twitch' in driver.current_url:
                    logger.info('Find twitch')
                    break
            else:
                driver.switch_to.window(driver.window_handles[0])
                logger.info('Failed to find twitch.')
        else:
            pass

        channel_info['channel_url'] = channel_url

    except WebDriverException:
        logger.warn('Chrome closed.')
        sys.exit()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
