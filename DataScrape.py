import bs4 as BeautifulSoup
import csv
from selenium import webdriver

def scrape(url,split):
    browser = webdriver.Firefox()
    browser.get(url)
    j = 0
    while (j < len(browser.find_elements_by_class_name("toggle-expansion"))):
        browser.find_elements_by_class_name("toggle-expansion")[j].click()
        j += 1

    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')
    table = soup.find_all('table',{"class":"stats-table stats-table-player"})[0]

    rows = table.find_all('tr')[1:]
    CSVfile = open("Player" + str(split) + ".csv", 'wt', newline='')
    writer = csv.writer(CSVfile)

    for row in rows:
        CSVrows = []
        for cell in row.find_all(['tr','td']):
            CSVrows.append(cell.get_text())
        writer.writerow(CSVrows)
        
    browser.find_elements_by_class_name("stats-nav-left")[1].click()
    
    
    while (j < len(browser.find_elements_by_class_name("toggle-expansion"))):
        browser.find_elements_by_class_name("toggle-expansion")[j].click()
        j += 1

    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')
    table = soup.find_all('table',{"class":"stats-table stats-table-team"})[0]

    rows = table.find_all('tr')[1:]
    CSVfile = open("Team" + str(split) + ".csv", 'wt', newline='')
    writer = csv.writer(CSVfile)

    for row in rows:
        CSVrows = []
        for cell in row.find_all(['tr','td']):
            CSVrows.append(cell.get_text())
        writer.writerow(CSVrows)
    browser.close()

scrape('https://fantasy.na.lolesports.com/en-US/league/803748/stats',1)
scrape('https://fantasy.na.lolesports.com/en-US/league/899089/stats',2)
scrape('https://fantasy.na.lolesports.com/en-US/league/1078350/stats',3)
scrape('https://fantasy.na.lolesports.com/en-US/league/1152480/stats',4)
scrape('https://fantasy.na.lolesports.com/en-US/league/1190618/stats',5)
scrape('https://fantasy.na.lolesports.com/en-US/league/1224700/stats',6)
scrape('https://fantasy.na.lolesports.com/en-US/league/1249782/stats',7)