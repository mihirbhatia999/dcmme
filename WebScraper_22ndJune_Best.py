
import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urltools
import time 




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
    exists = 0 
    try:
        request = requests.get(url)
        if request.status_code == 200:
            exists = 1 
            
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






# Accepting input of URL and depth----------------------------------------------
tic = time.time()
original_url = "https://www.rowetruck.com"
parent_list = [original_url]
url_to_check = get_base_url(original_url)
print(url_to_check)
url_to_check = str(url_to_check)

layer_stop = 1
layer = 0


#initializing all the requiered lists---------------------------------------------
visited_all  = [original_url]
visited_current_layer = []
child_list =[]
child_list_filtered = []
#columns = ['Link','Parent Link', 'Layer']
df = pd.DataFrame()


# Main execution of scrapper----------------------------------------------------

#looping through layers 
while layer < layer_stop:
    
    #looping through URLs in parent-list
    for url in parent_list:
        
        #scraping the children from the parent url----------------------------
        if href_scrapper(url) != 0:
            child_list = href_scrapper(url)
    
    
        for child in child_list:
            if child != None:
                #if child link is of the form "index.php/blahblah" and parent ends with '/'
                #---> "parentlink/index.php/blahblah"
                if child.startswith('/'):
                    child= str(url) + str(child)
                    
                if url.endswith('/') and url_to_check not in child:
                    child = str(url) + str(child)
                    
                #normalize the child links-------------------------------------
                child=urltools.normalize(child)  
                    

                #filtering out based on 1) External 2) Repeating 3) Invalid links---------------------------
                if url_to_check in child and child not in visited_all and does_page_exist(child)==1:
                    child_list_filtered.append(child)
                
                #adding everthing to visited all--------------------
                if child not in visited_all:
                    child_slash = child + '/'
                    visited_all.append(child)  
                    visited_all.append(child_slash)
                    
                    
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
    
    #we only dont add .png, .jpg , .pdf to the new parent layer 
    for visited_current in visited_current_layer: 
        print(visited_current)
        if(not visited_current.endswith('.png') and not visited_current.endswith('.jpg') and not  visited_current.endswith('.pdf')):
            parent_list.append(visited_current)
            
            
    #displaying the links in different layers----------------------------------
    #print("Links in LAYER:" + str(layer+1))
    print("No of links = " + str(len(visited_current_layer)))
    #print(visited_current_layer)
    print("\n")
    visited_current_layer = [] 
    #updating the layer number
    layer +=1
toc = time.time()
print(toc - tic)


tic = time.time()
href_scrapper("http://orijfowijfiwofij.com/")
toc = time.time()
print("href scrapper")
print(toc-tic)

tic = time.time()
does_page_exist("http://orijfowijfiwofij.com/")
toc = time.time()
print("does page exist")
print(toc-tic)


