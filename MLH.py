#Importing
from numpy.lib.function_base import append
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Declarations
Event_Names=[]
Event_Date=[]
Event_StartDate=[]
Event_EndDate=[]
Event_Link=[]
Event_Logo=[]
Event_Image=[]

#Get & Cleanup
url="https://mlh.io/seasons/2022/events"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
driver.get(url)
time.sleep(5)
html = driver.page_source
html=html.split("Past Events",1)[0]
html=html.split("Upcoming Events",1)[1]
soup = BeautifulSoup(html, "html.parser")

#Event Name
temp=soup.findAll(attrs={'class':'event-name'})
for hit in temp:
    Event_Names.append(hit.text)

#Event Date
temp=soup.findAll(attrs={'class':'event-date'})
for hit in temp:
    Event_Date.append(hit.text)

#Start Date
temp=soup.findAll(itemprop='startDate')
for hit in temp:
    Event_StartDate.append(hit.get("content"))

#End Date
temp=soup.findAll(itemprop='endDate')
for hit in temp:
    Event_EndDate.append(hit.get("content"))

#Event Link
temp=soup.findAll('a')
for hit in temp:
    Event_Link.append(hit.get('href'))

#Event Image
for div in soup.findAll('div','image-wrap'):
    for img in div.find_all('img'):
        Event_Image.append(img['src'])

#Event Logo
for div in soup.findAll('div','event-logo'):
    for img in div.find_all('img'):
        Event_Logo.append(img['src'])

#Writing Scraped Data to Dataframe
df=pd.DataFrame(Event_Names,columns=['Name'])
df['event-date']=Event_Date
df['event-start-date']=Event_StartDate
df['event-end-date']=Event_EndDate
df['event-link']=Event_Link
df['event-image']=Event_Image
df['event-logo']=Event_Logo

#Saving dataframe as CSV file
df.to_csv('data.csv',index=False)


driver.close()