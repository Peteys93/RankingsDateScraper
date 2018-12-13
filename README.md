# RankingsDataScraper
Rankings Data Scraper to Extract Date Information from rankings.the-elite.net

Current Version Data gathered - 12/12/2018 - 12/13/2018

Future plans, create a user interface to make selection of level, upper and lower bounds, and filename to save easier.

Current Use, in rankingsdatascraper.py
  edit high-points for upper bound of points info to scrape data, edit low points for lower bound of points info to scrape data
  e.g. high-points, low-points = 100, 60 -- will scrape all rankings data for personal bests between 100 and 60 points for the specified level

  edit filename to change the file that scraped data will be written to
  current use case is to write to a .csv and copy/paste manually into a .xlsx for data analysis
  
  edit url to determine stage - simply change the stagename to desired level to scrape
  e.g. aztec will scrape data from aztec, egypt will scrape data from egypt, etc.

  current excel file in Out/timeinfo - 60+.xlsx contains data for all personal best times worth 60 or more, instructions for pivot table use contained
  currently have manually colored the years for dam agent, secret agent and 00 agent