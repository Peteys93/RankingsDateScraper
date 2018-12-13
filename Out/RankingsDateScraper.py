import Funcs as scraper

#programs scrapes date information for chosen times on rankings.the-elite.net

#change the value of high_points for upper bound, low_points for lower bound of points to scrape, changefilename and url for filename and level to scrape from
high_points, low_points = 100, 95
filename = "\\timeinfo\\temp.csv"
url = "https://rankings.the-elite.net/goldeneye/stage/aztec"

#open file 'filename'
f = scraper.openfile(filename)

#open chrome browser at 'url'
driver = scraper.openbrowser(url)

#parse xml on rankspage and timespage to get personal best and date info
scraper.parse_xml(f, driver, high_points, low_points)

driver.quit()
f.close()