

from bs4 import BeautifulSoup


import os

##CHECKING LOCAL DB EXISTANCE 
SCRAPED_DATA_DB = "quora_scraped_data.csv"
if os.path.exists(SCRAPED_DATA_DB):
    print("File exists!")
else:
    with open(SCRAPED_DATA_DB,'w') as file:
        file.write('question,link,images,answers,username,userlink\n')
    print(f"File does not exist so creating {SCRAPED_DATA_DB}...")



def extract_related_answers(filename):
        
    with open(filename, "r") as f:
        html_content = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    elements = soup.find_all('div','Card___StyledBackroundTemporaryHighlightBoxChild-qc006b-0')
    filtered_elements  = [i for i in elements if 'dom_annotate_question_answer_item' in str(i)]
    # print(len(filtered_elements),'filtered...')
    # profile = soup.find_all('a',class_ = 'q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-color--gray_dark qu-cursor--pointer qu-hover--textDecoration--underline')
    # print(len(profile),'profiles')

    with open(SCRAPED_DATA_DB,'a') as file:
        for each_element in filtered_elements:
            try:
                question = each_element.find('span', class_ = 'q-text qu-truncateLines--5 puppeteer_test_question_title').text
                # print(text)
                question = question.replace(',','')

                links = each_element.find_all('a', class_ = 'q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-display--inline qu-cursor--pointer qu-hover--textDecoration--underline')
                hrefs = [link['href'] for link in links][0]
                # print(hrefs)

                answers = each_element.find('div', class_ = 'q-box spacing_log_answer_content puppeteer_test_answer_content').text
                answers = answers.replace(',','')

                image_data = each_element.find_all('img')
                img_srcs = [link['src'] for link in image_data if 'main-thumb' not in str(link)]
                # print(img_srcs)
                print('searching for name: ')

                profile = each_element.find('a',class_ = 'q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-color--gray_dark qu-cursor--pointer qu-hover--textDecoration--underline')
            
                # print(profile_name.text)
                profile_name = profile.text.strip().replace(',',' ')
                profile_url = profile['href'].strip().replace(',',' ')
                
                images = ' | '.join(img_srcs)
                
                file.write(f'{question},{hrefs},{images},{answers},{profile_name},{profile_url}\n')

                # print(f'{question},{hrefs},{images},{answers}\n')


            except Exception:
                # print('Related scraping Exception:::--',Exception)
                pass
                            
                




def extract_answers(answer_html_filename,url):

    # Open the HTML file
    with open(answer_html_filename, "r") as f:
        html_content = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    elements = soup.find_all('div','Card___StyledBackroundTemporaryHighlightBoxChild-qc006b-0')
    filtered_elements  = [i for i in elements if 'dom_annotate_question_answer_item' in str(i)]

    with open(SCRAPED_DATA_DB,'a') as file:
        for each_element in filtered_elements:
            try:
                href = url
                question = soup.find('div','q-text puppeteer_test_question_title').text
                question = question.replace(',','')
                answers = each_element.find('div', class_ = 'q-box spacing_log_answer_content puppeteer_test_answer_content').text
                answers = answers.replace(',','')
                image_data = each_element.find_all('img')
                img_srcs = [link['src'] for link in image_data if 'main-thumb' not in str(link)]
                # print(img_srcs)
                images = ' | '.join(img_srcs)
                print('searching for name: ')
                profile = each_element.find('a',class_ = 'q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-color--gray_dark qu-cursor--pointer qu-hover--textDecoration--underline')
                profile_name = profile.text.strip().replace(',',' ')
                profile_url = profile['href'].strip().replace(',',' ')

                file.write(f'{question},{href},{images},{answers},{profile_name},{profile_url}\n')

                

            except Exception:
                print('Answer scraping Exception:::--',Exception)
                
