# RankingsDataScraper
Rankings Data Scraper to Extract Date Information from rankings.the-elite.net

Current Use, in rankingsdatascraper.py
  edit high-points for upper bound of points info to scrape data, edit low points for lower bound of points info to scrape data
  e.g. high-points, low-points = 100, 60 -- will scrape all rankings data for personal bests between 100 and 60 points for the specified level

  edit filename to change the file that scraped data will be written to
  current use case is to write to a .csv and copy/paste manually into a .xlsx for data analysis
  
  edit url to determine stage - simply change the stagename to desired level to scrape
  e.g. aztec will scrape data from aztec, egypt will scrape data from egypt, etc.
