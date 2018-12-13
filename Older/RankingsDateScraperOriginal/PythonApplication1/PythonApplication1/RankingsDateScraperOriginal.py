from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

#programs scrapes date information for chosen time on rankings.the-elite.net
#everything here must be manually changed, TODO accept user input for level, difficulty, time, to allow easier data gathering

path = os.getcwd()

#open file, manually change name to desired
f = open(path + "\\dates\\cradeA34.csv","w") #FHSU

#launch url, manually change to desired page
url = "https://rankings.the-elite.net/goldeneye/stage/cradle"


#create a new Chrome session, change to location of your chromedriver install
driver = webdriver.Chrome(r"C:\Users\Patrick\Desktop\Programs\chromedriver.exe")
driver.implicitly_wait(30)
driver.get(url)

#manually copy xpaths from time links on page source to find range of links for time from which dates will be scraped for use in range() (tr[i](first time) - tr[i+1](last time))
for i in range(18,20):
    link_string_A = '//*[@id="diff-0"]/table/tbody/tr[' + str(i) + ']/td[3]/a[1]'
    #link_string_SA = '//*[@id="diff-1"]/table/tbody/tr[' + str(i) + ']/td[3]/a[1]'
    #link_string_00A = '//*[@id="diff-2"]/table/tbody/tr[' + str(i) + ']/td[3]/a[1]'
    
    #manually choose link string to use, A, SA, or 00A, uncomment chosen difficulty link_string above
    python_button = driver.find_element_by_xpath(link_string_A)
    python_button.click()

    #hand off xml to bs4 for parsing
    soup_level1=BeautifulSoup(driver.page_source, 'lxml')

    #find all ul items and store in a string, definitely a cleaner way to do this, but this works
    date = soup_level1.find_all("ul", id='time_details')
    date_string = str(date)

    #attempt to write date to file if date is listed, ignore if date is not on page
    if("<li><strong>Achieved:</strong> " in date_string):
        ds2 = date_string.split("<li><strong>Achieved:</strong> ")
        ds3 = ds2[1].split("</li>")
        print(ds3[0])
        f.write(ds3[0] + '\n')

    #click the back button
    driver.execute_script("window.history.go(-1)") 

driver.quit()
f.close()