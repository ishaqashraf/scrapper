from bs4 import BeautifulSoup
import requests
import sys
import re
import csv

# importing libraries
import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
from time import sleep, time


# function writing url in urls.txt file
def file_writer(data):
    with open('urls.txt', 'a', encoding="utf-8") as dataFile:
        dataFile.write(data + '\n')

#function writing data in data.csv file
def file_writers(data_array):
    with open('nn.csv', 'a', encoding="utf-8" , newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(data_array)


#function fetch data when all related channel fetched,then goes to unfetch channel and again fetch the data.
def fetch_urls1(url):
    #selenium driver get URl
    result1 = requests.get("http://youtube.com/channel/"+url+"/about")
    sleep(5)
    soup = BeautifulSoup(result1.content, 'html.parser')
    related_channels = soup.find_all("li",class_="branded-page-related-channels-item")
    x=0
    while x<len(related_channels):
        try:
            channel_url_id = related_channels[x]['href']
            channel_url = channel_url_id
            if (check_url_exist(channel_url)):
                x = x + 1;
                continue;
            print("43")
            fetch_urls(channel_url);
            res1 = requests.get(url)
            soup = BeautifulSoup(res1.content, 'html.parser')
            related_channels = soup.find_all("ytd-mini-channel-renderer",class_="style-scope ytd-vertical-channel-section-renderer")
            s = related_channels['href']
            x=x+1;
        except:
            channel_url_id = related_channels[x]['href']
            channel_url = channel_url_id
            if (check_url_exist(channel_url)):
                x = x + 1;
                continue;
            print("55")
            fetch_urls(channel_url);
            print("related fetch1 Exception")
        
    print("finished fetch 1")

#function fetch data from specific url and then go to related and featured channel and fatch data.
def fetch_urls(url):
    url1=url
    #selenium driver get URl
    result = requests.get(url+"/about")

    file_writer(url)


    # sleep(10)
    #bs4 getting content from selenium driver instance
    soup = BeautifulSoup(result.content, 'html.parser')
    data_to_excel = []
    title_container = soup.find_all("span",class_="qualified-channel-title-text")
    title = title_container[0].a.text
    print("Titile = " + title)
    print("url = " + url)
    #getting title 
    # title_container = soup.find_all("span", id="channel-title")
    # title = title_container[0].text
    #getting subscriber
    try:
        subscriber_container = soup.find_all("span", class_="about-stat")
        subscriber =subscriber_container[0].b.text 
    except:
        subscriber = "Not Found"
    # print("Title:" + title)
    # print("Channel Link:" + url)
    #print("Subcriber:" + subscriber)
    #getting description
    try:
	    about_container = soup.find_all("div",class_="about-description branded-page-box-padding")
	    about = about_container[0].text
    except:
        about = "No description Found"
    #print("Description:" + about)

    #Getting email
    soup1 = soup.prettify()
    try:
        emailfetch=soup1.split('"businessEmail":')[1]
        emailsplit=emailfetch.split('",')[0]
        email=emailsplit.split('"')[1]
    except:
        email="Not Found"
    if(email==""):
        email="not found"
    
    print("email :" + email)

    #getting country
    try:
        country_container = soup.find_all("div", class_="about-metadata-label about-metadata-label-border-top branded-page-box-padding")
        country = soup.find_all("span",class_="country-inline")[0].text
    except:
        country = "No Country found"
    print("Country:" + country+"\n")

    #getting social links    
    try:
        socials_array = []
        for each in soup.find_all("a",class_="about-channel-link"):
            socials_array.append(each.attrs['title'] + ": " + each.attrs['href'])

        all_socials = '\n'.join(socials_array)
    except:
        all_socials = "Not Found"
    #print("All Social:" + all_socials)

    #data written in excel file 
    data_to_excel.extend([title,url,subscriber,country,email,about,all_socials])
    file_writers(data_to_excel)
   #go to related channel div
    related_channels = soup.find_all("li",class_="branded-page-related-channels-item")
    print(len(related_channels))
    x=0
    while x<len(related_channels):
        try:
            channel_url_id = related_channels[x]['data-external-id']
            channel_url = channel_url_id
            if (check_url_exist(channel_url)):
                x = x + 1;
                continue;
            print("139")
            b = "http://youtube.com/channel/"+channel_url
            fetch_urls(b);
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            related_channels = soup.find_all("li",class_="branded-page-related-channels-item")
            x=x+1;
        except:
            a = "http://youtube.com/channel/"+channel_url
            print("147")
            fetch_urls(a);
           
    print("=========================================")
    #get unfetch channel and again start fetching
    print("153")
    fetch_urls1(url1)
    print("finished fetch")
    

# this function will check if specified url exist in file or not
def check_url_exist(url_to_check):
    # open the file using `with` context manager, it'll automatically close the file for you
    with open("urls.txt") as f:
        found = False
        for line in f:  # iterate over the file one line at a time(memory efficient)
             if re.search(url_to_check, line):   #if string found is in current line then print it
                print("already there")
                found = True
        return found


# this will RUN when the script will starts
if __name__ == "__main__":
    #initializing driver object for selenium
    # chrome_options = Options()  
    # chrome_options.add_argument("--headless")  
    # driver = webdriver.Chrome(r"C:\Users\ishaq\Desktop\chrome\chromedriver.exe")
    url = "https://www.youtube.com/channel/UCoykjkkJxsz7JukJR7mGrwg"
    if (check_url_exist(url)):
        print("url exists in main body")
        fetch_urls(url)
    else:
        fetch_urls(url)
    
