import requests as rq
from requests.exceptions import Timeout

from bs4 import BeautifulSoup as bs

def decorate(text:str,num:int):
    print(text*num)

url="https://www.trendyol.com/sr?q="

i=input("Search for any products on Trendyol: ")

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
    

    #all products for search keyword are is in <div class:prdct-cntnr-wrppr> box element
    raw=soup.find('div',{'class':'prdct-cntnr-wrppr'})

    #links=raw.find_all("div",{"class":"p-card-chldrn-cntnr"})
    links=raw.find_all("a",href=True)
    links=[pt["href"] for pt in links]
    
    name_price=raw.find_all(["div"],{"class":["prdct-desc-cntnr-ttl-w","product-price"]})
    name_price=[pt.get_text() for pt in name_price]
    
    #display the results
    print("\nRESULTS for",i)
    for a in range(0,len(name_price)-2,2):
        print(" Name: {}\n      Price: {}\n            Link: www.trendyol.com{}".format( name_price[a], name_price[a+1], links[a//2] ) )
        decorate("<>",40)
    """
    prices=raw.find_all("div",{"class":"product-price"})
    prices=[pt.get_text() for pt in prices]
    print("prices\n",prices)
    
    print("\nRESULTS for",i)
    decorate("=",80)
    for a,b in zip(names,prices):
        print("Product:",a,"Price:",b)
        decorate("<>",40)
    """
else:
    print(page.status_code)
