import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import MySQLdb

def insert_to_database(sql_command, values):
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="network_analysis",
                         charset='utf8')
    try:
        print "CONNECTION SUCCESSFUL"
        cursor = db.cursor()

        try:
            cursor.execute(sql_command, values)
            db.commit()
            "Insert Data!"
        except Exception, e:
            print(e)
            db.rollback()
        # Close the connection
        db.close()
    except MySQLdb.Error:
        print "ERROR IN CONNECTION"

### Set language in Selenium
options = webdriver.ChromeOptions()
options.add_argument('--lang=es')
browser = webdriver.Chrome("C:\chromedriver.exe",chrome_options=options)
browser.get('https://www.google.com/maps/dir/')

df = pd.read_csv('input/2_convertScoreToRating.csv', index_col=0)

pathList = []

for i in tqdm(df.index):
    for j in range(i+1,max(df.index)+1):
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

                time.sleep(5)
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
            
            field_name = ('origin','target','originId','targetId','time','method','distance')
            sql = u'INSERT INTO chiangmai_distance(' + ','.join(field_name) + ') VALUES (%s, %s, %s, %s, %s, %s, %s);'
            infoList = [df.loc[i,'place'],df.loc[j,'place'],i,j,shortest_time,method,shortest_dist]
            insert_to_database(sql, infoList)
            print("From: ", df.loc[i,'place'], " To: ", df.loc[j,'place'], " With: ", method, " In: ", shortest_time)

            ### Append to list
            pathList.append(infoList)

column_names = ['origin','target','originId','targetId','time','method','distance']

path = pd.DataFrame(pathList, columns=column_names)
print(path.head())
path.to_csv('input/3_timeDistanceList.csv')