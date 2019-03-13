import bs4 as BeautifulSoup
import csv
from selenium import webdriver

#importing important libraries (obviously)

browser = webdriver.Firefox()
URL_Summer2015 = 'https://fantasy.na.lolesports.com/en-US/league/803748/stats'
browser.get(URL_Summer2015)
j = 0
while (j < 172):
    browser.find_elements_by_class_name("toggle-expansion")[j].click()
    j += 1

# starting the browser window through the selenium firefox webdriver, travelling to the website, and expanding the table to get week-by-week stats rather than just the totals


innerHTML = browser.execute_script("return document.body.innerHTML")
soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')
table = soup.find_all('table',{"class":"stats-table stats-table-player"})[0]

# scraping the table



rows = table.find_all('tr')[1:]
CSVfile = open("test.csv", 'wt', newline='')
writer = csv.writer(CSVfile)

for row in rows:
    CSVrows = []
    for cell in row.find_all(['tr','td']):
        CSVrows.append(cell.get_text())
    writer.writerow(CSVrows)

# writing the table data into a csv file 
print("done")
browser.close()