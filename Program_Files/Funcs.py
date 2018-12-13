from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import time

#open file, manually change name to desired
def openfile(filename):
    f = open(os.getcwd() + filename, 'a')
    return f

#launch url, manually change to desired page
def openbrowser(url):
    #create a new Chrome session
    driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
    driver.implicitly_wait(30)
    driver.get(url)     
    time.sleep(3) #wait for page to load, increase number if connection is slow, if desired, decrease if fast
    return driver

#parse rankings page xml with bs4 to get Time, Points, then click on time link to get Date/Level/Name info from next page
def parse_xml(f, driver, high_points, low_points):
    soup_level0=BeautifulSoup(driver.page_source, 'lxml')

    #Offset by ten from top 10 leaders      
    parse_points = soup_level0.find_all(class_="points")
    points_string = str(parse_points)
    points= re.findall("\d+", points_string)

    #parse agent, sa, and 00a times, store for later, add up lengths of the lists for later use as well    
    time_agent = soup_level0.find_all("div", id="diff-0")
    time_string_agent = str(time_agent)
    ts_agent = re.findall(">\d+:\d\d+|N\/A", time_string_agent) #must have > here as start char and take out later, to avoid picking up other numbers on page

    time_secret_agent = soup_level0.find_all("div", id="diff-1")
    time_string_secret_agent = str(time_secret_agent)
    ts_secret_agent = re.findall(">\d+:\d\d+|N\/A", time_string_secret_agent)

    time_00_agent = soup_level0.find_all("div", id="diff-2")
    time_string_00_agent = str(time_00_agent)
    ts_00_agent = re.findall(">\d+:\d\d+|N\/A", time_string_00_agent)

    ag_times = len(ts_agent)
    ag_sa_times = len(ts_agent) + len(ts_secret_agent) 
    total_times = len(ts_agent) + len(ts_secret_agent) + len(ts_00_agent)

    #loop through all times in agent, secret agent, and 00 agent lists
    i, offset = 0, 0    
    while i <= total_times:     
        if(int(points[i]) <= high_points and int(points[i]) >= low_points): # change high_points and low_points in rankingsdatascraper.py for upper/lower bound        
            if i < ag_times: # get link and time string for agent, set isa True for printing/writing
                link_string = '//*[@id="diff-0"]/table/tbody/tr[' + str(i-offset+2) + ']/td[3]/a[1]' #offset by number of points leaders, +2 here because tr[2] is first item we want to click in each column
                ts_agent[i-offset] = re.sub(">", "", ts_agent[i-offset])
                time_string = ts_agent            
                isa, issa, is00a = True, False, False
            elif i >= ag_times and i < ag_sa_times: # get link and time string for secret agent, update bools for print/write
                link_string = '//*[@id="diff-1"]/table/tbody/tr[' + str(i-ag_times-offset+2) + ']/td[3]/a[1]'
                ts_secret_agent[i-ag_times-offset] = re.sub(">", "", ts_secret_agent[i-ag_times-offset])
                time_string = ts_secret_agent            
                isa, issa, is00a = False, True, False
            elif i >= ag_sa_times and i < total_times: # get link and time string for 00agent, update bools for print/write
                link_string = '//*[@id="diff-2"]/table/tbody/tr[' + str(i-ag_sa_times-offset+2) + ']/td[3]/a[1]'
                ts_00_agent[i-ag_sa_times-offset] = re.sub(">", "", ts_00_agent[i-ag_sa_times-offset])
                time_string = ts_00_agent            
                isa, issa, is00a = False, False, True
            
            #click the link given by the xpath for the link_string set above    
            python_button = driver.find_element_by_xpath(link_string)
            python_button.click()

            #parse - times page xml with bs4 for to get Name, Date, and Level Name/Difficulty
            soup_level1=BeautifulSoup(driver.page_source, 'lxml')

            #parse - zoom closer to name, level, and date on timespage, probably a better way to parse this for cleaner regex, but this works
            parse_name = soup_level1.find_all(class_='user')
            parse_level = soup_level1.find_all("h1")
            parse_date = soup_level1.find_all("ul")            
            
            name_string = str(parse_name)
            level_string = str(parse_level)
            date_string = str(parse_date)

            ns2 = re.findall("[>][\w][A-Za-z\u00fc\-\s]*", name_string)
            name_string_final = re.sub("[>]", "", str(ns2[0]))

            ls2 = re.findall("[\t][A-Z][a-z]+[012A-Za-z\s\t]*[Agent\t]+", level_string)
            ls3 = re.sub("[\t]", " ", str(ls2[0]))
            level_string_final = ls3.strip()
                      
            #check if date is listed, set to blank space if not listed.
            if("<li><strong>Achieved:</strong> " in date_string):
                date_string = date_string.split("<li><strong>Achieved:</strong> ")
                date_string_final = date_string[1].split("</li>")
            else:
                date_string_final[0] = ""        
        
            #print to cmd and file, alter time string for a, sa, and 00a
            if isa:
                print(name_string_final, level_string_final, time_string[i-offset], points[i], date_string_final[0])
                f.write(name_string_final + ',' + level_string_final + ',' + time_string[i-offset] + ',' +   points[i] + ',' + date_string_final[0] + '\n')
            elif issa:
                print(name_string_final, level_string_final, time_string[i-ag_times-offset], points[i], date_string_final[0])
                f.write(name_string_final + ',' + level_string_final + ',' + time_string[i-ag_times-offset] + ',' +   points[i] + ',' + date_string_final[0] + '\n')
            elif is00a:
                print(name_string_final, level_string_final, time_string[i-ag_sa_times-offset], points[i], date_string_final[0])
                f.write(name_string_final + ',' + level_string_final + ',' + time_string[i-ag_sa_times-offset] + ',' +   points[i] + ',' + date_string_final[0] + '\n')

            #go back when finished parsing date/name/level info to allow the program to move onto the next link
            driver.execute_script("window.history.go(-1)")
        elif int(points[i]) > 100: # set the offset based on the number of points leaders at the top of the page (as they are read into the 'points' parse from earlier)
            offset += 1
        i += 1