import csv
import datetime
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#read list of string from a text file and store them in an array


class SearchResult:
    def __init__(self, title, date,authors,contentType,link,notes):
        self.title = title
        self.date = date
        self.authors = authors
        self.contentType = contentType
        self.link = link
        self.notes = notes


def extractDataFromHtml(isDate, results, htmlFilePath):
    data = open(htmlFilePath,'r',encoding="utf-8")
    soup = BeautifulSoup(data, 'html.parser')
# Parse the HTML content with BeautifulSoup
#soupWeb = BeautifulSoup(html_content, "html.parser")

# Find the ordered list element <ol> in the HTML content
    l_comp = soup.find_all("article", {'class': "search-result-item"})


    for li_element in l_comp:
        link = li_element.find_all("a")[0].attrs["href"]
        summary = ""
        authors = ""
        date = ""
        
        try:
            summary = li_element.find("p").text
        except:
            summary = "NOT FOUND"
        try:
            authors = li_element.find("span",{'class': "name"}).text
        except:
            authors = "NONE"
        try:
            date = li_element.find("div",{'class': "time"}).text
        except:
            date = "NO DATE"
        try:
            title = li_element.find("div",{'class': "title"}).text
        except:
            title = "NO TITLE"
            print("NO TITLE")
            print(li_element.text)

        res = SearchResult(title=title,date=date,authors=authors,contentType="Game developer",link=link,notes=summary)
        results.append(res)
            
        
        

# Open a CSV file for writing
def writeCsv(results, csvFilePath):
    with open(csvFilePath, "w",encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)

    # Write each list item element to the CSV file
        for res in results:
            writer.writerow([res.title, res.date, res.authors, res.contentType, res.link, res.notes])

def isDate(text):
    try:
        datetime.datetime.strptime(text, '%b %d, %Y')
        return True
    except ValueError:
        return False

def saveHtmlWithFullScrolledTable(url,fileName,numberOfScrolls):
    chromrdriver = "./chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromrdriver
    driver = webdriver.Chrome(chromrdriver)
    driver.get(url)

    
    for i in range(1,numberOfScrolls):
        driver.execute_script("window.scrollTo(1,50000)")
        time.sleep(1)

    file = open(fileName, 'w',encoding="utf-8")
    file.write(driver.page_source)
    file.close()

    driver.close()
    

url = "https://www.gamedeveloper.com/search?q=%28test%20OR%20testing%20OR%20tests%29&sort=newest&terms=programming&terms=design&terms=art&terms=production&types=article"
results = []

htmlFilePath = "./DSC"".html"

# saveHtmlWithFullScrolledTable(url,htmlFilePath,100)

extractDataFromHtml(isDate, results, htmlFilePath)

writeCsv(results,"./GDSearchResults.csv")
        

