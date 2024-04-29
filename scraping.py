from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values
import platform
current_directory = os.getcwd()
env = dotenv_values(os.path.join(current_directory, 'env', '.env'))

USERNAME = env.get("USERNAME")
PASSWORD = env.get("PASSWORD")

download_directory = current_directory
current_os = platform.system()

chrome_options = Options()
chrome_options.add_argument(f"--download.default_directory={download_directory}")
chrome_options.add_argument("--headless")

if current_os == "Windows":
    chrome_driver_path = "chromedriver.exe"
elif current_os=='Linux':
    chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
else:
    print(f"Unsupported operating system: {current_os}")


driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=chrome_options)

time.sleep(2)
try:
    driver.get("https://netportal.hdfcbank.com/login")
    print("Navigated to HDFC Bank website.")

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "liabiltyLoginCustId"))
    )
    username_field.send_keys(USERNAME)
    print("Entered username.")

    login_button = driver.find_element(By.ID, "continuelogin")
    login_button.click()
    print("Clicked login button.")

    time.sleep(2)

    password_field = driver.find_element(By.ID, "keyboard")
    password_field.send_keys(PASSWORD)
    print("Entered password.")

    password_login_button = driver.find_element(By.ID, "loginBtn")
    password_login_button.click()
    print("Clicked password login button.")

    time.sleep(3)

    summary = driver.find_element(By.CLASS_NAME, "detail-info")
    summary.click()
    print("Clicked summary.")

    time.sleep(3)

    transactionDropDown = driver.find_element(By.XPATH, "//div[@placeholder='Please select a duration']")
    transactionDropDown.click()
    print("Clicked transaction duration dropdown.")

    transactionDuration = driver.find_element(By.ID, "ui-select-choices-row-0-1")
    transactionDuration.click()
    print("Selected transaction duration.")

    time.sleep(2)

    downloadButton = driver.find_element(By.XPATH, "//a[@ng-click='accountsStatementCtrl.download()']")
    downloadButton.click()
    print("Clicked download button.")
    time.sleep(1)

    selectTypeDropdown = driver.find_element(By.XPATH, "//div[@class='modal-body two clearfix accounts-nb']//span[@class='ui-select-match-text pull-left']")
    selectTypeDropdown.click()
    print("Clicked select type dropdown.")

    selectType = driver.find_element(By.ID, "ui-select-choices-row-1-3")
    selectType.click()
    print("Selected type.")

    time.sleep(1)

    finalDownload = driver.find_element(By.XPATH, "//div[@class='modal-body two clearfix accounts-nb']/div/a")
    finalDownload.click()
    print("Clicked final download.")
    time.sleep(2)

    logout = driver.find_element(By.XPATH, "//a[@ng-click='logout();']")
    logout.click()
    print("Clicked logout.")
    time.sleep(1)

    yesButton = driver.find_element(By.XPATH, "//a[@class='btn btn-primary nb-logout yes-btn']")
    yesButton.click()
    print("Clicked yes button.")
    time.sleep(2)

except Exception as e:
    print(e)
    logout = driver.find_element(By.XPATH, "//a[@ng-click='logout();']")
    logout.click()
    print("Clicked logout.")
    time.sleep(1)

    yesButton = driver.find_element(By.XPATH, "//a[@class='btn btn-primary nb-logout yes-btn']")
    yesButton.click()
    print("Clicked yes button.")
    time.sleep(2)
driver.quit()

env_directory = os.path.join(download_directory, 'env')

files = os.listdir(download_directory)

downloaded_files = [file for file in files if file.endswith('.DELIMITED')]

if downloaded_files:
    os.rename(os.path.join(download_directory, downloaded_files[0]),
              os.path.join(env_directory, downloaded_files[0].replace('.DELIMITED', '.csv')))
    print("File extension changed successfully.")
else:
    print("No file with .DELIMITED extension found.")

env_files = os.listdir(env_directory)

if os.path.exists(os.path.join(env_directory, 'transactions.csv')):
    os.remove(os.path.join(env_directory, 'transactions.csv'))
transaction_files = [file for file in env_files if file.endswith('.csv') and file.startswith('Acct')]
os.rename(os.path.join(env_directory, transaction_files[0]),
        os.path.join(env_directory, 'transactions.csv'))
print("Transactions file renamed successfully.")

