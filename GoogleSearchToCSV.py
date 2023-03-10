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


with open("urls.txt", "r") as f:
    urls = f.read().splitlines()

    




def extractDataFromHtml(isDate, results, htmlFilePath):
    data = open(htmlFilePath,'r',encoding="utf-8")
    soup = BeautifulSoup(data, 'html.parser')
# Parse the HTML content with BeautifulSoup
#soupWeb = BeautifulSoup(html_content, "html.parser")

# Find the ordered list element <ol> in the HTML content
    l_comp = soup.find("div", {'id': "rso"}).contents


    for li_element in l_comp:
        link = li_element.find_all("a")[0].attrs["href"]
        
        try:
            title = li_element.find("h3").text
            spans = li_element.find_all("span")
            date = ""
            for span in spans:
                if isDate(span.text):
                    date = span.text
                    break
            res = SearchResult(title=title,date=date,authors="",contentType="google search",link=link,notes="")
            results.append(res)
        except:
            print("discard:")
            print(li_element.text)

            
        
        

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
        time.sleep(5)

    file = open(fileName, 'w',encoding="utf-8")
    file.write(driver.page_source)
    file.close()

    driver.close()
    

# saveHtmlWithFullScrolledTable(url2,"./DS.html",1)
results = []
page = 1
for url in urls:
    htmlFilePath = "./DS"+str(page)+".html"
    saveHtmlWithFullScrolledTable(url,htmlFilePath,1)
    extractDataFromHtml(isDate, results, htmlFilePath)
    page+=1


    


writeCsv(results,"./googleSearchResults.csv")
        

