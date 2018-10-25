import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import urltools
import time
#import smtplib
from pandas import ExcelWriter
from pandas import ExcelFile

import time
import json
import urllib
import os
path = 'W:\pu.data\Desktop\Scrapper_to_use'
os.chdir(path)

from urllib.parse import urljoin

def get_base_url(url):
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))


    if base_url.startswith("https"):
        base_url = base_url.replace('https://','')
    elif base_url.startswith("http"):
        base_url = base_url.replace('http://','')

    if base_url.endswith('/'):
        base_url = base_url.replace('/','')
    return base_url


def does_page_exist(url):
    exists = 1
    try:
        request = requests.get(url)
        if request.status_code == 404:
            exists = 0

    except:
        pass

    return exists


# Function to extract links from a URL------------------------------------------
def href_scrapper(url):

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        a_tag = soup.find_all('a')
        img_tag = soup.find_all('img')
        link_tag = soup.find_all('link')
        link_list = list()

        for links in a_tag:
            link_list.append(links.get('href'))

        for links in link_tag:
            link_list.append(links.get('href'))

        for links in img_tag:
            link_list.append(links.get('src'))

        return link_list

    except:
        return 0


# Function to create complete links---------------------------------------------
def link_former(url):
    x = url

    if x.startswith("http"):
        return x

    else:
        full_url = original_url + x
        return full_url


# Function to save links to directory of python file----------------------------
def file_save(url, i):
    save_error = 0
    full_url = url
    try:
        if str(full_url).endswith(".htm"):
            name = "WebPage" + str(i) + ".htm"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        elif str(full_url).endswith(".pdf"):
            name = "Pdf" + str(i) + ".pdf"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        elif str(full_url).endswith(".jpg"):
            name = "Image" + str(i) + ".jpg"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        elif str(full_url).endswith(".jpeg"):
            name = "Image" + str(i) + ".jpeg"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        elif str(full_url).endswith(".png"):
            name = "Image" + str(i) + ".png"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        elif str(full_url).endswith(".css"):
            name = "CSS File" + str(i) + ".css"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        else:
            name = "WebPage" + str(i) + ".html"
            urllib.request.urlretrieve(full_url, name)
            m = i + 1

        return m
    except:
        save_error = save_error + 1



'''
crawl function = takes link as input and crawls relevant webpages from the parent 

Inputs 
----------

Outputs
----------
'''
def crawl(original_url, num_Id, output_file):

    # Accepting input of URL and depth----------------------------------------------
    tic = time.time()

    parent_list = [original_url]
    url_to_check = get_base_url(original_url)
    print(url_to_check)
    url_to_check = str(url_to_check)

    layer_stop = 1
    layer = 0


    #initializing all the required lists---------------------------------------------
    visited_all  = [original_url]
    visited_current_layer = []
    child_list =[]
    child_list_filtered = [original_url]
    #columns = ['Link','Parent Link', 'Layer']
    df = pd.DataFrame()

    Di={}

    # Main execution of scrapper----------------------------------------------------

    #looping through layers
    while layer < layer_stop:

        #looping through URLs in parent-list
        for url in parent_list:

            #scraping the children from the parent url----------------------------
            href_url = href_scrapper(url)
            if href_url != 0:
                child_list = href_url


            for child in child_list:
                if child != None:
                    ch=child
                    #if child link is of the form "index.php/blahblah" and parent ends with '/'
                    #---> "parentlink/index.php/blahblah"
                    #if child.startswith('/'):
                        #child= str(url) + str(child)
                    #if url.endswith('/') and url_to_check not in child:
                        #child = str(url) + str(child)

                    child = urljoin(url,child)

                #normalize the child links-------------------------------------
                    child=urltools.normalize(child)
                    social_media = ['facebook.com','google.com','reddit.com','linkedin.com','github.com','twitter.com','digg.com','tumblr.com''.png', '.jpg','.jpeg', '.pdf', '.css']

                    #filtering out based on 1) External 2) Repeating 3) Invalid  4) social media + pdf + css ---------------------------
                    #if url_to_check in child and child not in visited_all and does_page_exist(child)==1 and ch not in Di:
                    if url_to_check in child and child not in visited_all and ch not in Di and all(social not in child for social in social_media):
                        child_list_filtered.append(child)
                        Di[ch]=1

                    #adding everything to visited all--------------------
                    if child not in visited_all:
                        child_slash = child + '/'
                        visited_all.append(child)
                        visited_all.append(child_slash)

                #sleep-------------------------------------------------------
                time.sleep(0.250)

            #adding  the visited and filtered children into the "current visited layer" ------
            for child_filtered in child_list_filtered:
                visited_current_layer.append(child_filtered)

            #creating a Pandas dataframe to store everything for download----------

            layer_number = [layer+1]*len(child_list_filtered)
            parent_of_child = [url]*len(child_list_filtered)

            df_child = pd.DataFrame(child_list_filtered)
            df_parent = pd.DataFrame(parent_of_child)
            df_layer = pd.DataFrame(layer_number)


            df_to_be_added = pd.concat([df_child,df_parent,df_layer], axis=1)
            df = pd.concat([df,df_to_be_added],ignore_index=True, axis = 0)


            #----------------------------------------------------------------------

            #emptying the child lists
            child_list = []
            child_list_filtered = []

        #condition to stop filtering-----------------------------------------------
        if not visited_current_layer :
            layer_stop = layer_stop
        else:
            layer_stop += 1


        #child layer is now parent layer--------------------------------------------
        parent_list = []

        for visited_current in visited_current_layer:
            print(visited_current)
            #if(not visited_current.endswith(unwanted_extensions)):
            parent_list.append(visited_current)


        #displaying the links in different layers----------------------------------
        #print("Links in LAYER:" + str(layer+1))
        print("No of links = " + str(len(visited_current_layer)))
        #print(visited_current_layer)
        print("\n")
        visited_current_layer = []
        #updating the layer number
        layer +=1
    df.to_csv(output_file + '/' + str(num_Id) + '_' + str(url_to_check) +  '.csv', sep=',', encoding='utf-8')
    return df, num_Id


#-----------------------------------------------------------------------------

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    header += 'Cc: %s' % ','.join(cc_addr_list)
    header += 'Subject: %s' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

#---------------------------------------------------------------------------
'''
Functions that will be used by the scraper function 
tag_visible = 
text_from_html = 
'''

import requests
page = requests.get("https://docs.python.org/3/howto/urllib2.html")
from bs4 import BeautifulSoup
from bs4.element import Comment
soup = BeautifulSoup(page.content, 'html.parser')


#information based on:
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
p_tag=soup.find_all('p')

#extract text from html:
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
web_text = []

#---------------------------------------------------------------------------



def scrape(df, scraped_website_path, website_index, website_name):
    extensions=('.png', '.jpg','.jpeg','.pdf', '.gif','.ico', '.mp4')
    TempD={}
    for index,item in df.iterrows():
        #print(item[1],item[0])
        try:
            #for i in extensions:
            #print(item[1])
            if any(x in item[1] for x in list(extensions)):
            #if item[1].endswith(extensions):
                print(item[1],"skipped because image/gif/pdf")
                print(" ")

            elif ".gif&" in item[1]:
                print(item[1],"skipped because contains &gif")
                print(" ")

            elif "facebook.com" in item[1] or "linkedin.com" in item[1] or "twitter.com" in item[1]:
                print(item[1], "skipped because social network link")
                print(" ")

            else:
                print(item[1])
                print(" ")
                html = urllib.request.urlopen(item[1]).read()
                #web_text.append(text_from_html(html))
                print(text_from_html(html))
                time.sleep(1)
                #save_url(str(item[1]), index)
                TempD[item[1]]=text_from_html(html)
        #label: end
        except:
            pass
    with open(scraped_website_path + '/' + 'json_' + str(website_index) + str(get_base_url(website_name)) +  '.json', 'w') as outfile:
        json.dump(TempD, outfile)

    return 1



# web_crawler_all() = Scraper for multiple websites# web_crawler
'''
Inputs
-----------
excel_path = Excel file path which contains list of websites to be crawled  
sheet = sheet name of this excel file 
web_col = the column no of in which the website hompages are located 
index_col = the column with indices of websites
parent_col = the column with the parent names
output_folder = path of the output folder where we wish to save the websites 
from_website = the index no. from website (typically starting from 1)
to_website = the index no of the website till we want to continue scraping (scraped websites will include the 
                websites with this index)

Output 
-----------
CSV files containing a list of child links for each website are saved into the output_folder path 

'''
def web_crawler_all(excel_path, sheet, web_col, index_col, parent_col,  output_folder, from_website, to_website):
    df = pd.read_excel(excel_path , sheet_name=sheet)
    df = df.iloc[from_website-1 : to_website, :]

    for index,row in df.iterrows():

        num_Id=int(row[index_col])
        original_url=row[web_col]

        tic = time.time()
        try:
            websites, num_Id = crawl(original_url ,num_Id ,output_folder)
            #websites= pd.read_csv(output_folder + '/' + str(int(num_Id)) + '_' + str(original_url) + '.csv')
            #print("website is already crawled")
        except:
            pass

        toc = time.time()
        print("Time taken to crawl all links: "  + str(toc - tic))

    print("All links from the websites indicated have been crawled")
    print("Output File :  " + str(output_folder))
    print("No. of websites scraped : " + str(to_website - from_website + 1))
    return 1


'''
Inputs 
----------
excel_path = Excel file path which contains list of websites to be crawled  
sheet = sheet name of this excel file 
crawled_website_path = path of file where all the crawled websites are stored  
scraped_website_path = path of file where all the scraped websites are stored
from_website - to_website = website index number from-to which we want to scrape and store in JSON 
web_col = column number of websites (0,1,2....)

Output
----------
JSON files for each parent website in scraped_website_path folder. The path of the scraped websites 
is the same as that crawled websites 
'''

def web_scraper_all(df, crawled_website_path, scraped_website_path, from_website, to_website,web_col):
    #get excel sheet containing websites
  #  df = pd.read_excel(excel_path , sheet_name=sheet)
    df = df.iloc[from_website-1 : to_website, :]

    #loop over all the websites and extract child links. Store them in JSON files

    for index, rows in df.iterrows():
        #setting the website index and name
        website_index = int(rows[0])
        website_name = rows[web_col]
        filename = crawled_website_path + '/'+ str(website_index)+ '_' + str(get_base_url(website_name)) + ".csv"

        #generating filename and getting the csv file of child links

        df_of_child_links = pd.read_csv(filename)
        print(filename,df_of_child_links )
        #executing the scrape function
        flag = scrape(df_of_child_links , scraped_website_path, website_index, website_name)

        #checkpoint to see if scraping is complete
        if flag == 1 :
            print(website_name + ' has been scraped successfully')
            #print('scraping percentage complete = ' + str((i/to_website)*100) + '%')
            flag = 0


#executing the crawler function ---------------------------------------------------------------------------------------

excel_path = 'batchwise_companies.xlsx'
sheet = 'batch36'
web_col = 2
index_col = 0
parent_col = 1
output_folder = 'Crawled'
from_website = 1
to_website = 1

web_crawler_all(excel_path,sheet, web_col, index_col, parent_col,output_folder, from_website, to_website)

#send mail--------------------------------------------------------------------------------------------------------------
'''
sendemail(from_addr = 'krannertdcmme@gmail.com', to_addr_list = ['mihirbhatia999@gmail.com'],
          cc_addr_list = ['djindal@purdue.edu'],subject = 'Test mail',message = 'this is a test mail 2 using Python',
          login = 'krannertdcmme', password = 'Abc12345!', smtpserver = 'smtp.gmail.com:587')
print("email sent")
'''


#executing the scraper function-----------------------------------------------------------------------------------------
excel_path = 'batchwise_companies.xlsx'
sheet = 'batch36'
df = pd.read_excel(excel_path , sheet_name=sheet)
crawled_website_path = 'Crawled'
scraped_website_path = 'Scraped'
from_website = 1
to_website = 1
web_col = 2 
#print(df)
web_scraper_all(df, crawled_website_path, scraped_website_path, from_website, to_website,web_col)

#send mail
'''
sendemail(from_addr = 'krannertdcmme@gmail.com', to_addr_list = ['mihirbhatia999@gmail.com'],
          cc_addr_list = ['djindal@purdue.edu'],subject = 'Test mail',message = 'this is a test mail 2 using Python',
          login = 'krannertdcmme', password = 'Abc12345!', smtpserver = 'smtp.gmail.com:587')
'''
# function to crawl + scrape everything-------------------------------------------------------------------

'''
def whin_crawl_scrape(excel_path = 'batchwise_companies.xlsx',from_sheet ,to_sheet ,crawled_website_path = 'Crawled',scraped_website_path = 'Scraped',web_col = 2):
    df = pd.read_excel(excel_path)
    for i in range(from_sheet, to_sheet + 1):
        sheet = 'batch' + str(i)
        web_crawler_all(excel_path,sheet, web_col = web_col, index_col = 0, parent_col =1 ,output_folder=crawled_website_path,
                        from_website = 1 , to_website = df.shape[0] + 1)
        web_scraper_all(df, crawled_website_path, scraped_website_path, from_website = 1, to_websitedf.shape[0] + 1,
                        web_col= web_col)

    sendemail(from_addr = 'krannertdcmme@gmail.com', to_addr_list = ['mihirbhatia999@gmail.com'],
          cc_addr_list = ['djindal@purdue.edu'],subject = 'Test mail',message = 'this is a test mail 2 using Python',
          login = 'krannertdcmme', password = 'Abc12345!', smtpserver = 'smtp.gmail.com:587')



### FINAL FUNCTION -------------------------------------------------------------------------------------------------------
whin_crawl_scrape(excel_path = 'batchwise_companies.xlsx',from_sheet = 1 ,to_sheet = 1 ,crawled_website_path = 'Crawled',
                      scraped_website_path = 'Scraped',web_col = 2)
'''

