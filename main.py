import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from db_dump import *


def save_html_pages(quora_url):

    try:

        chrome_driver_path = './chromedriver_mac64/chromedriver'
        service = ChromeService(executable_path=chrome_driver_path)

        # create a new Chrome session
        driver = webdriver.Chrome(service=service)

        # navigate to the Quora website
        driver.get(quora_url)

        driver.implicitly_wait(5)
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

        actions = ActionChains(driver)
        elements = driver.find_elements(By.CLASS_NAME,'puppeteer_test_read_more_button')
        #if the click is performed from front consecutive elements are chaning so doing from back 
        elements.reverse()
        for ele in elements:
            print(ele.text)
            actions.move_to_element(ele)
            print('Continue read clicked....')
            actions.click()
            actions.perform()
        url = quora_url.split('https://www.quora.com/')[-1]
        ## RELATED ANSWERS WRITTEN TO FILE
        related_answers_file = f'related_{url}.html'
        # print(related_answers_file)
        with open(f'html_pages/{related_answers_file}', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
            print('related_written to file')

        ####### DUMP RELATED TO DB
        extract_related_answers(f'html_pages/{related_answers_file}')

        ## FINDING THE ALL RELATED BUTTON AND CLICK ON IT
        print('came to check all related..')
        elements = driver.find_elements(By.CLASS_NAME,'qu-ellipsis')
        for element in elements:
            if 'All related' in element.text:
                actions.move_to_element(element)
                actions.click()
                actions.perform()
                # element.click()
                print('clicked')
                break
        print('came to click answers')
        ##CLICK ANSWER AFTER FINDING ALL RELATED
        driver.execute_script("document.getElementsByClassName('q-text qu-dynamicFontSize--small qu-color--gray_dark')[1].click();")

        time.sleep(3)
        answers_html_file = f'answer_{url}.html'
        with open(f'html_pages/{answers_html_file}', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
            print('answers to file')

        ####### DUMP ANSWERS TO DB
        extract_answers(f'html_pages/{answers_html_file}',url=quora_url)

        # sentinal_input = input("Press Enter to exit: ")
        driver.quit()
    except Exception:
        print('Look at this exception please....',Exception)



def main():
    with open('trailurls.txt') as file:
        urls = file.readlines()
    for url in urls:    
        try:
            print('Processing : ',url)
            save_html_pages(url)
        except:
            print(f'cannot do for url:  {url}')
            with open('failed.txt','a') as failedfile:
                failedfile.write(url+'\n')
    # save_html_pages('https://www.quora.com/Why-do-more-people-visit-Tirupati-Balaji-Temple-than-other-Hindu-temples')
main()