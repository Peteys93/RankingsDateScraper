from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import time

#open file, manually change name to desired
def openfile(filename):
    f = open(os.getcwd() + filename, 'a')
    if not os.path.getsize(os.getcwd() + filename) > 0:
        f.write("Name,Level,Time,Points,Date,Year\n")
    return f

#launch url, manually change to desired page
def openbrowser(url):
    driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
    driver.implicitly_wait(30)
    driver.get(url)     
    time.sleep(3) #wait for page to load, increase number if connection is slow, if desired, decrease if fast
    return driver

#parse rankings page xml with bs4 to get Time, Points, then click on time link to get Date/Level/Name info from next page
def parse_xml(f, driver, high_points, low_points, select_a, select_sa, select_00a):
    soup_level0=BeautifulSoup(driver.page_source, 'lxml')

    #parse points
    points = [p.text.strip() for p in soup_level0.select(".stage-table .points")]

    #parse agent, sa, and 00a times, store for later, add up lengths of the lists for later use as well    
    ts_agent = [a.text.strip() for a in soup_level0.select("#diff-0 .time")]
    ts_secret_agent = [b.text.strip() for b in soup_level0.select("#diff-1 .time")]
    ts_00_agent = [c.text.strip() for c in soup_level0.select("#diff-2 .time")]    

    ag_times, ag_sa_times, total_times = len(ts_agent), len(ts_agent) * 2, len(ts_agent) * 3

    #loop through all times in agent, secret agent, and 00 agent lists
    i = 0
    while i < total_times:     
        if(int(points[i]) <= high_points and int(points[i]) >= low_points):
            doClick = False #Dont click the link to parse the next page if loop doesn't go into any of these if statements
            if i < ag_times and select_a: # get link and time string for agent, set isa True for printing/writing, first tr in times list is 2, set doClick true if link is set
                link_string, time_string = '//*[@id="diff-0"]/table/tbody/tr[' + str(i+2) + ']/td[3]/a[1]', ts_agent        
                isa, issa, is00a, doClick = True, False, False, True
            elif (i >= ag_times and i < ag_sa_times) and select_sa: #secret agent
                link_string, time_string = '//*[@id="diff-1"]/table/tbody/tr[' + str(i-ag_times+2) + ']/td[3]/a[1]', ts_secret_agent                          
                isa, issa, is00a, doClick = False, True, False, True
            elif (i >= ag_sa_times and i < total_times) and select_00a: #00/perfect agent
                link_string, time_string = '//*[@id="diff-2"]/table/tbody/tr[' + str(i-ag_sa_times+2) + ']/td[3]/a[1]', ts_00_agent           
                isa, issa, is00a, doClick = False, False, True, True
                        
            #click the link given by the xpath for the link_string set above    
            if(doClick):
                python_button = driver.find_element_by_xpath(link_string)
                python_button.click()

                #parse - times page xml with bs4 for to get Name, Date, and Level Name/Difficulty
                soup_level1=BeautifulSoup(driver.page_source, 'lxml')

                #parse - name, level, and date on timespage
                name_string_final = soup_level1.select_one("#content .user").text.encode('ascii', errors ='ignore').strip().decode('ascii')

                parse_level = soup_level1.select_one("#content > h1").text.strip()
                level_string = re.split("\t\d:", parse_level)
                level_string_final = level_string[0].replace("\t", " ")
                
                parse_date = soup_level1.select_one("#time-details > li").text.strip()
                date_string_final, year_string_final = "", "" #no date or year by default
                if "Achieved" in parse_date: #if date on page
                    date_string_final = parse_date.replace("Achieved: ", "")
                    year_string_final = re.search('\d{4}', date_string_final).group() #extract year to remove extra step in excel for pivot chart
        
                #print to cmd and file, alter time string for a, sa, and 00a
                if isa and select_a:
                    print(name_string_final, level_string_final, time_string[i], points[i], date_string_final)
                    f.write(name_string_final + ',' + level_string_final + ',' + time_string[i] + ',' +   points[i] + ',' + date_string_final + ',' + year_string_final + '\n')
                elif issa and select_sa:
                    print(name_string_final, level_string_final, time_string[i-ag_times], points[i], date_string_final)
                    f.write(name_string_final + ',' + level_string_final + ',' + time_string[i-ag_times] + ',' +   points[i] + ',' + date_string_final + ',' + year_string_final + '\n')
                elif is00a and select_00a:
                    print(name_string_final, level_string_final, time_string[i-ag_sa_times], points[i], date_string_final)
                    f.write(name_string_final + ',' + level_string_final + ',' + time_string[i-ag_sa_times] + ',' +   points[i] + ',' + date_string_final + ',' + year_string_final + '\n')

                #go back when finished parsing date/name/level info to allow the program to move onto the next link
                driver.execute_script("window.history.go(-1)")          
        i += 1