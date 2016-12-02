#!/usr/local/bin/python3.4
'''
Created on 2-Dec-2016

@author: kapil
'''

import webbrowser, sys, pyperclip,requests,os,bs4,re
foldername='cyanide and Happiness' #default
absAddress='http://explosm.net'  #default
def downloadFile(filename,foldername,res):
    downloadDirectry='/home/kapil/Downloads/comics'
    fileDirectory=downloadDirectry+'/'+foldername
    os.makedirs(fileDirectory, exist_ok=True)  #create folder for downloaded files
    file = open(os.path.join(fileDirectory, filename), 'wb')
    for chunk in res.iter_content(100000):
            file.write(chunk)

           
def checkValidLinks(linkElems):
    
    validlinks=[]
    if(type=='pdf'):
        for l in linkElems:
            trueLink=re.split(r'&',l.get('href'))
            filename, fileExt = os.path.splitext(trueLink[0])
            print(fileExt)
            #print(l.get('href'))
            if fileExt=='.pdf':
                validlinks.append(l.get('href'))
               
        
    if(type=='ppt'):
        for l in linkElems:
            filename, fileExt = os.path.splitext(l.get('href'))
            if fileExt=='.ppt'|'.pptx':
                validlinks.append(l.get('href'))
    return validlinks
    
        
def requestPage(urlAddress):
   # webbrowser.open(str(urlAddress))
    try:
        res = requests.get(urlAddress)
    except Exception as exc:
        print('There was a problem in getting destination file: %s' % (exc)) 
        print('trying again...')
        return requestPage(urlAddress)
    return res 


def getComicWebsiteLink(comicName):
    if(comicName=='cyanide'):
        foldername='cyanide and Happiness'
        absAddress='http://explosm.net'
        return 'http://explosm.net/comics/latest' 
    return 'http://explosm.net/comics/1715/' 
def getComicId(comicLink):
    return (str(comicLink).split('?')[0]).split('/')[-1]


def getComicLink(pageFile):
    soup = bs4.BeautifulSoup(pageFile.text,"html.parser")
    img=soup.find('img', {'id': 'main-comic'})
    if(img==None):
        img= img=soup.find('div', {'class': 'small-12 medium-12 large-12 columns'}).find('embed')
    print(img)
    comicLink=str(img['src'])
    if(comicLink.split('/')[0]!='http:'):
        comicLink='http:'+comicLink
    return comicLink

def getNextPageLink(pageFile):
    soup = bs4.BeautifulSoup(pageFile.text,"html.parser")
    for div in soup.findAll('div', {'class': 'medium-8 columns end'}):
        a = div.findAll('a')[1]
    print ( a.attrs['href'])
    nextPageLink = str(a.attrs['href'])
    return nextPageLink
            
if len(sys.argv) > 1:
# Get address from command line.
    comicName = str(sys.argv[1]).lower()
    
    
else:
# Get address from clipboard.
    comicName = pyperclip.paste()
    comicName=str(comicName.split(sep=' ')[0]).lower()
        
    #add file type to enhance more result oriented search
urlAddress=getComicWebsiteLink(comicName)


 #open the link in google
#webbrowser.open(urlAddress)
res=requestPage(urlAddress)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
    
    
soup = bs4.BeautifulSoup(res.text,"html.parser")
for div in soup.findAll('div', {'class': 'medium-8 columns end'}):
    a = div.findAll('a')[0]
    print ( a.attrs['href'])
oldestPageLink = str(a.attrs['href'])
oldestPageLink=absAddress+oldestPageLink
oldestPage=requestPage(oldestPageLink)
oldestcomicLink=getComicLink(oldestPage)
oldestComicId=getComicId(oldestcomicLink)
    
    
pageLink=urlAddress


while True:
    pageFile=requestPage(pageLink)
    comicLink=getComicLink(pageFile)
    currentComicId=getComicId(comicLink)
    print(currentComicId)
    downloadFile(currentComicId, foldername, requestPage(comicLink))
    if(currentComicId==oldestComicId):
        break
    pageLink=getNextPageLink(pageFile)
    pageLink=absAddress+pageLink


    
    
    