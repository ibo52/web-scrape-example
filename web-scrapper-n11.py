import requests as rq
from requests.exceptions import Timeout

from bs4 import BeautifulSoup as bs

def decorate(text:str,num:int):
    print(text*num)

url="https://www.n11.com/arama?q="

i=input("Search for any products on N11: ")

headers=[{
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',},
         {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
}]

timeouts=(4.6 , 6.5)#connect,response timeout

try:
    page=rq.get(url+i,headers=headers[0], timeout=timeouts)
except Timeout as e:
    print(e,": server connect/reply waited too long.")
    exit(e)

if page.status_code==200:#means OK

    soup=bs(page.content,"html.parser")

    products=[]

    #all products for search keyword are is in <ul class:list-ul> box element on the website
    raw=soup.find('ul',{'class':'list-ul'})
    #print(soup.prettify()

    #print( products[0].prettify() )

    links=raw.find_all("a",{"class":"plink"})
    links=[pt["href"] for pt in links]
    
    names=raw.find_all("h3",{"class":"productName"})
    names=[pt.get_text() for pt in names]

    prices=raw.find_all("ins")
    prices=[pt.get_text() for pt in prices]

    print("\nRESULTS for",i)
    decorate("=",80)
    for a,b,c in zip(names,prices,links):
        print("Product:",a)
        print("Price:",b)
        print("Link:",c)
        decorate("<>",40)
    
else:
    print(page.status_code)
