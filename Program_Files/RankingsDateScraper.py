import Funcs as scraper

#programs scrapes date information for chosen times on rankings.the-elite.net

#change the value of high_points for upper bound, low_points for lower bound of points to scrape,
#set select_* false to ignore times from that difficulty
#change game and level for game and level to scrape from
#change filename to desired .csv file

high_points, low_points = 100, 95 
select_a, select_sa, select_00a = True, True, True 
game, level = "perfect-dark", "extraction" 
filename = "test3.csv" 

f = scraper.openfile("\\out\\" + filename)

#open chrome browser at 'url'
driver = scraper.openbrowser("https://rankings.the-elite.net/" + game + "/stage/" + level)

#parse xml on rankspage and timespage to get personal best and date info
scraper.parse_xml(f, driver, high_points, low_points, select_a, select_sa, select_00a)

driver.quit()
f.close()