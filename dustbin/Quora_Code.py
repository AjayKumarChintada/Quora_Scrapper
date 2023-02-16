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


# email_id = driver.find_element('id','email')
email_id.click()
email_id.send_keys('ajaykumar.chintada@gytworkz.com')

password = driver.find_element('id', 'password')
password.click()
password.send_keys('Iamtherare123@@')


# login_button = driver.find_element('class','q-text qu-ellipsis qu-whiteSpace--nowrap')
password.click()
driver.implicitly_wait(3)
password.send_keys(Keys.ENTER)
print("LOGGED IN")

driver.get('https://www.quora.com/topic/Temples')
print('Opened the temples topic')
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

#get all the html data 
html = driver.page_source

with open('page.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

# parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# find elements using BeautifulSoup
elements = soup.find_all('span', class_='q-box qu-userSelect--text')
print(elements)
print(len(elements))

questions = [i.text for i in elements]
print(questions,len(questions))



sentinal_input = input("Press Enter to exit: ")
driver.quit()



#more class in div tag
# q-text qu-cursor--pointer QTextTruncated__StyledReadMoreLink-sc-1pev100-2 bSoNWX qt_read_more qu-color--blue_dark qu-fontFamily--sans qu-pl--tiny