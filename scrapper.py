# importing all the necessary libraries
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
import re
from selenium.webdriver.common.keys import Keys


import urllib.parse
from urllib.parse import urlparse
import randomAgent
from selenium import webdriver

from time import sleep
# defining the googleSearch function

def googleSearch(num, query):
    # making the url ready for requests
    url = 'https://scholar.google.com/scholar?start={}&client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(num,
                                                                                                               query)
    # generating a random user agent using the randomAgent function we previously defined
    user_agent = randomAgent.getUA()
    # defining header for the request function
    ran_head = {
        'user-agent': user_agent,
    }
# declaring list g_clean to store the fetched urls
    g_clean = []
    # exception handling code to make sure we don't run into errors
    try:
        # fetching the response using get method in requests
        html = requests.get(url)
        # checking the response status to be success
        if html.status_code == 200:
            # parsing the fetched html in the response using lxml parser in beautiful soup
            soup = BeautifulSoup(html.text, 'lxml')
            # finding all the 'a' tags, links, in the parsed html
            a = soup.find_all('a')
            # looping through the all found a tags for processing
            for i in a:
                # extracting the href attribute for the link to the search results
                k = i.get('href')
                # exception handling code to prevent running into erros
                try:
                    # search for the pattern of a url to prevent unneccessary attributes in the result using re module
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    # fetching only the url part in the array
                    n = m.group(0)
                    # splitting the url upto the parameters part to get only the necessary url
                    rul = n.split('&')[0]
                    # parsing the url to divide it into components using urlparse
                    domain = urlparse(rul)
                    # checking if the fetched url belongs to google.com if true skip the url
                    if(re.search('google.com', domain.netloc)):
                        continue
                    # else add it to the result list
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    # finally return the result urls
    finally:
        return g_clean
def aclweb(query):
    # making the url ready for requests
    query = query.split(' ')
    query= '+'.join(query)
    print(query)
    url = 'https://www.aclweb.org/anthology/search/?q={}'.format(query)
    # generating a random user agent using the randomAgent function we previously defined
    print(url)
    browser = webdriver.Chrome('./chromedriver')
    browser.get(url)
    sleep(4)
   
    # declaring list g_clean to store the fetched urls
    g_clean = []
    # exception handling code to make sure we don't run into errors
    try:
        html = browser.page_source
        browser.close()
        if True:

            # parsing the fetched html in the response using lxml parser in beautiful soup
            soup = BeautifulSoup(html, 'lxml')
            # finding all the 'a' tags, links, in the parsed html
            a = soup.find_all('a')            
            # looping through the all found a tags for processing
            for i in a:
                # extracting the href attribute for the link to the search results
                k = i.get('href')
                # exception handling code to prevent running into erros
                try:
                    # search for the pattern of a url to prevent unneccessary attributes in the result using re module
                    m = re.search("(?P<url>https?://[^\s]+)", k)

                    # fetching only the url part in the array
                    n = m.group(0)
                    # splitting the url upto the parameters part to get only the necessary url
                    rul = n.split('&')[0]
                    # parsing the url to divide it into components using urlparse
                    domain = urlparse(rul)
                    # checking if the fetched url belongs to google.com if true skip the url
                    if(re.search('google.com', domain.netloc)):
                        continue
                    # else add it to the result list
                    else:
                        g_clean.append(rul)
                except:
                    continue
 
    # finally return the result urls
    finally:
        return g_clean

def science_direct(query):
    # making the url ready for requests
    query = query.split(' ')
    query= '%20'.join(query)
    url = 'https://www.sciencedirect.com/search?qs={}'.format(query)
    # generating a random user agent using the randomAgent function we previously defined
    browser = webdriver.Chrome('./chromedriver')
    browser.get(url)
    sleep(10)
    g_clean = []
    # exception handling code to make sure we don't run into errors
    try:
        html = browser.page_source
        browser.close()
        if True:

            # parsing the fetched html in the response using lxml parser in beautiful soup
            soup = BeautifulSoup(html, 'lxml')
            # finding all the 'a' tags, links, in the parsed html
            a = soup.find_all('a',class_ = 'download-link')            
            # looping through the all found a tags for processing
            for i in a:
                print(i)

                # extracting the href attribute for the link to the search results
                k = i.get('href')   
                k= 'https://www.sciencedirect.com'+ k  
                print(k)
           # exception handling code to prevent running into erros
                try:
                
                    g_clean.append(k)
                except:
                    continue
 
    # finally return the result urls
    finally:
        return g_clean


if __name__ == "__main__":
    
    topic_list = ["pos nlp"]  # list of topic you want to search
    dir_link = 'pdfs/'  # dir where you want to store
    max_num_of_pdf = 20





    for topic in topic_list:
        num=0
        lis = set(science_direct(topic)+aclweb(topic))
        for i in lis:
            if re.search('.pdf$', i) or re.search('pdf', i):
                try:
                    num = num+1
                    print('downloading', i, '\n')
                    urlretrieve(i, dir_link + topic+'_' + str(num)+'.pdf')
                except:
                    print('this link contains error')
                if num==max_num_of_pdf:
                    break
    for topic in topic_list:
        num = 0
        link_page = 0
        while(link_page < max_num_of_pdf):
            lis1 = set(googleSearch(link_page, topic))
            link_page = link_page+10
            for i in lis1:
                if i in lis:
                    continue
                print(i)
                if re.search('.pdf$', i) or re.search('pdf', i):
                    try:
                        num = num+1

                        print('downloading', i, '\n')
                        urlretrieve(i, dir_link + topic+'_' + str(num)+'.pdf')
                    except:
                        print('this link contains error')
                print(num)
                if num == max_num_of_pdf:
                    break
         