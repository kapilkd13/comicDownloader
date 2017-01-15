#!/usr/local/bin/python3.4
'''
Created on 6-Jan-2017

@author: kapil
'''

import webbrowser, sys, pyperclip,requests,os,bs4,re
foldername='Calvin and Hobbes' #default
absAddress='http://www.gocomics.com'  #default
def downloadFile(filename,foldername,res):
    downloadDirectry='/home/kapil/Downloads/comics' #put your download directory here
    fileDirectory=downloadDirectry+'/'+foldername
    os.makedirs(fileDirectory, exist_ok=True)  #create folder for downloaded files
    file = open(os.path.join(fileDirectory, filename), 'wb')
    for chunk in res.iter_content(100000):
            file.write(chunk)
 
        
def requestPage(urlAddress):
   # webbrowser.open(str(urlAddress))
    try:
        res = requests.get(urlAddress, headers={'User-Agent' : "Magic Browser"})#this site don't allow python scripts to make request
    except Exception as exc:
        print('There was a problem in getting destination file: %s' % (exc)) 
        print('trying again...')
        return requestPage(urlAddress)
    return res 


def getComicWebsiteLink(comicName):
    return 'http://www.gocomics.com/calvinandhobbes/1994/01/01' 
    
def getComicId(comicLink):
    return (str(comicLink).split('?')[0]).split('/')[-1]


def getComicLink(pageFile):
    soup = bs4.BeautifulSoup(pageFile.text,"html.parser")
    imgbox=soup.find('picture', {'class': 'img-fluid item-comic-image'})
    img=imgbox.findAll('img')[0]
    print(img)
    comicLink=str(img['src'])
    if(comicLink.split('/')[0]!='http:'):
        comicLink='http:'+comicLink
    return comicLink

def getNextPageLink(pageFile):
    soup = bs4.BeautifulSoup(pageFile.text,"html.parser")
    div2= soup.find('div', {'class': 'button-icon-group'})
    a = div2.findAll('a', {'class': 'fa btn btn-outline-default btn-circle fa-caret-left sm '})[0]
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

    

#find out oldest comic id
#when runnig this script to download only new comics set the oldestComicId var to latest comic id you have downloaded
soup = bs4.BeautifulSoup(res.text,"html.parser")
div= soup.find('div', {'class': 'button-icon-group'})

a = div.findAll('a', {'class': 'fa btn btn-outline-default btn-circle fa-backward sm '})[0]
print ( a.attrs['href'])
oldestPageLink = str(a.attrs['href'])
oldestPageLink=absAddress+oldestPageLink
oldestPage=requestPage(oldestPageLink)
oldestcomicLink=getComicLink(oldestPage)
oldestComicId=getComicId(oldestcomicLink)
print(oldestComicId+"dsf")   
    
pageLink=urlAddress
#9350ac30df8d01317256005056a9545d 1992
#2e827ca0dece013171ac005056a9545d 1990
#9bd16e60dec10131719a005056a9545d 1988
#03f33460deb801317193005056a9545d 1986
oldestComicId='2e827ca0dece013171ac005056a9545d'
while True:
    pageFile=requestPage(pageLink)
    comicLink=getComicLink(pageFile)
    print(comicLink)
    currentComicId=getComicId(comicLink)
    print(currentComicId)
    downloadFile(currentComicId, foldername, requestPage(comicLink))
    if(currentComicId==oldestComicId):
        break
    pageLink=getNextPageLink(pageFile)
    pageLink=absAddress+pageLink
    


    
    
    