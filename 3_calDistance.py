import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

### Set language in Selenium
options = webdriver.ChromeOptions()
options.add_argument('--lang=es')
browser = webdriver.Chrome("C:\chromedriver.exe",chrome_options=options)
browser.get('https://www.google.com/maps/dir/')

df = pd.read_csv('input/2_convertScoreToRating.csv', index_col=0)

pathList = []

for i in tqdm(df.index):
    for j in df.index:
        if i == j:
            pass
        else:
            try:
                time.sleep(5)
                start = browser.find_element_by_xpath("//div[@id='directions-searchbox-0']//input")
                start.clear()
                start.send_keys(df.loc[i,'place'])
                
                time.sleep(2)
                dest = browser.find_element_by_xpath("//div[@id='directions-searchbox-1']//input")
                dest.clear()
                dest.send_keys(df.loc[j,'place'])
                
                time.sleep(1)
                ### Press Enter key
                dest.send_keys(u'\ue007')

                time.sleep(3)
                page = BeautifulSoup(browser.page_source,"html5lib")

                div_main = page.find("div", {"id":"section-directions-trip-0"})
                #print(div_main)

                div_method = div_main.find("div")
                method = div_method.get('class','')[1]
                #print(div_method.get('class','')) # -> [u'section-directions-trip-travel-mode-icon', u'walk']

                time_distance = div_main.find("div", {"class":"section-directions-trip-duration"})
                shortest_time = time_distance.text.strip()

                distance = div_main.find("div", {"class":"section-directions-trip-distance section-directions-trip-secondary-text"})
                shortest_dist = distance.text.strip()
                
                start.clear()
                dest.clear()
                
            except:
                shortest_dist = ""
                method = ""

            print("From: ", df.loc[i,'place'], " To: ", df.loc[j,'place'], " With: ", method, " In: ", shortest_time)

            ### Append to list
            pathList.append([df.loc[i,'place'],df.loc[j,'place'],i,j,shortest_time,method,shortest_dist])

column_names = ['origin','target','originId','targetId','time','method','distance']

path = pd.DataFrame(pathList, columns=column_names)
print(path.head())
path.to_csv('input/3_timeDistanceList.csv')