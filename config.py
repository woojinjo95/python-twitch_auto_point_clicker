import os
user_name = os.getlogin()
base_dirname = os.path.dirname(__file__)


chrome_executable_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
base_chrome_download_url = 'https://chromedriver.storage.googleapis.com'
chromedriver_version_check_site = 'https://chromedriver.chromium.org/downloads'
chromedriver_zipfile_name = 'chromedriver_win32.zip'
chromedriver_executable_name = 'chromedriver.exe'
user_path = os.path.join(base_dirname, 'usr')
