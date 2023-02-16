import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# specify the path to the chromedriver executable
chrome_driver_path = './chromedriver_mac64/chromedriver'
service = ChromeService(executable_path=chrome_driver_path)
# create a new Chrome session
driver = webdriver.Chrome(service=service)
# navigate to the Quora website
driver.get("https://www.quora.com/")
wait = WebDriverWait(driver, 10)
email_id = wait.until(EC.presence_of_element_located((By.ID, "email")))
email_id.click()
email_id.send_keys('ajaykumar.chintada@gytworkz.com')
password = driver.find_element('id', 'password')
password.click()
password.send_keys('Iamtherare123@@')
password.click()
driver.implicitly_wait(3)
password.send_keys(Keys.ENTER)
print("LOGGED IN")


##TOPIC URL 
URL = 'https://www.quora.com/topic/Temples'

topic = URL.split('topic/')[-1]

driver.get(URL)
print(f'Opened the {topic} topic')
driver.implicitly_wait(2)

driver.refresh()
print('Refreshing..')
driver.implicitly_wait(2)

count = 0
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    print()
    count += 1
    print(f'{count} - Scrolling....')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("Breaking the scroll")
        break
    last_height = new_height


if count<7:
    print('Trying second reload')
    driver.refresh()
    count=0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print()
        count += 1
        print(f'{count} - Scrolling....')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Breaking the scroll")
            break
        last_height = new_height



#get all the html data 
html = driver.page_source

with open(f'topic_{topic}.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

# # parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')


links = soup.find_all('a', class_="q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline")
                                   
# Extract the href attributes of each link
hrefs = [link['href'] for link in links]

with open('topic_urls.txt','a') as file:
    for i in hrefs:
        if i.startswith('https://www.quora.com'):
            file.write(f'{i}\n')


sentinal_input = input("Press Enter to exit: ")
driver.quit()

