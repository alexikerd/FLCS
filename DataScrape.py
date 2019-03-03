import bs4 as BeautifulSoup
import csv
from selenium import webdriver

#importing important libraries (obviously)

browser = webdriver.Firefox()
URL_Summer2015 = 'https://fantasy.na.lolesports.com/en-US/league/803748/stats'
browser.get(URL_Summer2015)

# starting the browser window through firefox as well as setting up the url


innerHTML = browser.execute_script("return document.body.innerHTML")
browser.close()

# this is where the main issue is located.  the resulting html is parsed correctly however it only parses the totals.  
# I want to parse the extra hidden information that pops up when you press the pluses at the side of the table 
# (after i manually press it, inspecting the element finally shows the stats I want)  I just need to know how to activate 
# all the buttons through the selenium web driver efficiently.  Viewing the source code every event in order to expand
# the row for each player has the exact same .js path.  So, instead of performing mouse click actions there should be
# some way to perform a "for row in" with the js script on each row using selenium and then perform the webscraping
# I'm essentially asking for your advice because I have no experience with html (although I've learned a lot) let alone
# traversing javascript and source code



soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')




table = soup.find_all('table',{"class":"stats-table stats-table-player"})[0]
rows = table.find_all('tr')[1:]
CSVfile = open("Summer2015.csv", 'wt', newline='')
writer = csv.writer(CSVfile)
for row in rows:
    CSVrows = []
    for cell in row.find_all(['tr','td']):
        CSVrows.append(cell.get_text())
    writer.writerow(CSVrows)

# this is also pretty straightforward in that I'm writing the parsed information into a csv file.  
