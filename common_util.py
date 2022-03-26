import logging


logger = logging.getLogger('main')

def try_click(driver, keyword, find_method='id'):
    if find_method == 'id':
        screens = driver.find_elements_by_id(keyword)
    else:
        screens = driver.find_elements_by_class_name(keyword)
    try:
        if len(screens) > 0:
            logger.info(f'find keyword {keyword} by {find_method}')
            screens[0].click()
        else:
            logger.info('No matced elements.')
    except Exception as e:
        logger.info('fail to click')
        pass
