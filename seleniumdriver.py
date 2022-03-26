# consider windows only

import logging
import os
import re
import requests
import shutil
import subprocess
from datetime import datetime
from urllib.error import HTTPError

import wget

logger = logging.getLogger('main')

basepath = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(basepath, 'Chromedriver')
edgedriver_path = os.path.join(basepath, 'Edgedriver')
os.makedirs(chromedriver_path, exist_ok=True)
base_chrome_download_url = 'https://chromedriver.storage.googleapis.com'
base_edge_download_url = 'https://msedgedriver.azureedge.net'
chromedriver_version_check_site = 'https://chromedriver.chromium.org/downloads'
edgedriver_version_check_site = 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver'
chromedriver_zipfile_name = 'chromedriver_win32.zip'
edgedriver_zipfile_name = 'edgedriver_win64.zip'
chromedriver_executable_name = 'chromedriver.exe'
edgedriver_executable_name = 'msedgedriver.exe'
chrome_executable_path = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
if not os.path.exists(chrome_executable_path):
    chrome_executable_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

edge_executable_path = r'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
if not os.path.exists(edge_executable_path):
    edge_executable_path = r'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'


def get_subprocess_output(cmd, output_type='out'):
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            out = process.stdout.read().decode() if process.stdout else ''
            error = process.stderr.read().decode() if process.stderr else ''

        if output_type == 'out':
            return out
        elif output_type == 'error':
            return error
        else:
            return '\n'.join((out, error))
    except:
        return None


def wget_download(download_url, out):
    wget.download(download_url, out=out)
    logger.info(f'Download file from {download_url}')


def get_current_browser_version(executable_path):
    cmd = f'wmic datafile where \'name="{executable_path}"\' get Version /value'
    try:
        out = get_subprocess_output(cmd)
        version = out.split('=')[1].strip('\r\n')
        return version
    except Exception as e:
        logger.error(e)
        return None


def get_current_seleniumdriver_version(path, executable_name):
    executable = os.path.join(path, executable_name)
    if not os.path.exists(executable):
        logger.warn(f'Cannot found {executable}. initial download')
        return None
    cmd = f'{executable} --version'
    try:
        out = get_subprocess_output(cmd)
        version = out.split()[1]
        return version
    except Exception as e:
        logger.error(e)
        return None


def get_available_prime_version_driver(prime_version, check_site):
    try:
        scraped_text = requests.get(check_site).text
        pattern = re.compile(f'{prime_version}\.\d+\.\d+\.\d+')
        version = re.search(pattern, scraped_text).group()
        logger.info(f'Alternative version: {version}')
        return version
    except Exception as e:
        logger.error(e)
        return None


def update_seleniumdriver(driver_path, seleniumdriver_version, browser_version, base_download_url, seleniumdriver_zipfile_name, check_site):
    day = datetime.strftime(datetime.now(), '%Y-%m-%d')
    driver_name = os.path.basename(driver_path)
    # 가장 하위 버전 다른건 무시
    if not seleniumdriver_version or seleniumdriver_version.split('.')[:3] != browser_version.split('.')[:3]:
        requested_prime_version = browser_version.split('.')[0]

        logger.info(f'Update {seleniumdriver_version} to {browser_version}')
        download_url = f'{base_download_url}/{browser_version}/{seleniumdriver_zipfile_name}'
        try:
            try:
                wget_download(download_url, driver_path)
            except HTTPError:
                if not seleniumdriver_version or requested_prime_version != seleniumdriver_version.split('.')[0]:
                    logger.warn(f'Specific version({browser_version}) is not exist. try to find similar version')
                    browser_version = get_available_prime_version_driver(requested_prime_version, check_site)
                    download_url = f'{base_download_url}/{browser_version}/{seleniumdriver_zipfile_name}'
                    wget_download(download_url, driver_path)
                else:
                    logger.info(f'Same prime version and driver version not exists.')
                    logger.info(
                        f'Current {driver_name} version: {seleniumdriver_version} (alternative version of {browser_version})')
                    return

            zip_file_name = os.path.join(driver_path, seleniumdriver_zipfile_name)
            shutil.unpack_archive(zip_file_name, extract_dir=driver_path)
            os.remove(zip_file_name)
        except HTTPError:
            logger.error(f'Driver version is not matched and cannot find prime version file! ({day})')
        except Exception as e:
            logger.error(f'Version not exists or failed to install({day}): {e}')
    else:
        logger.info(f'Current {driver_name} version: {seleniumdriver_version}')


def update_chrome():
    chromedriver_version = get_current_seleniumdriver_version(chromedriver_path, chromedriver_executable_name)
    chrome_version = get_current_browser_version(chrome_executable_path)
    update_seleniumdriver(chromedriver_path, chromedriver_version, chrome_version,
                          base_chrome_download_url, chromedriver_zipfile_name, chromedriver_version_check_site)
