import requests as rq
from requests.exceptions import Timeout

from bs4 import BeautifulSoup as bs

def decorate(text:str,num:int):
    print(text*num)

url="https://www.amazon.com.tr/s?k="

i="i5 11400"#input("Search for any products on Amazon TR: ")

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

    #s-result-item
    #all products(+ another things) wrapper
    raw=soup.find('div',{'class':'s-main-slot s-result-list s-search-results sg-row'})

    #all products boxes
    raw=raw.find_all("div",{"data-component-type":"s-search-result"})

    name=[]
    links=[]
    price=[]
    for product_box in raw:

        #select prices
        z=product_box.select("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")

        #there are multiple same link on product box element.so one is fine
        z=z[0]["href"]
        
        #select clas:a-size-base-plus.a-color-base.a-text-normal inside box(description)
        y=product_box.select("span.a-size-base-plus.a-color-base.a-text-normal")
        y=y[0].get_text()
        
        #select class:a-offscren from span class(price)
        x= product_box.select("span.a-offscreen");
        if len(x)==0:
            x="TUKENDI"
            
        else:
            #if there is two price, then one of its is products
            #old price
            x=[a.get_text() for a in x]
            
        price.append( x )
        name.append( y )
        links.append( z )

    """
    #links=raw.find_all("div",{"class":"p-card-chldrn-cntnr"})
    links=raw.find_all("a",{"class":"a-link-normal"},href=True)
    links=[pt["href"] for pt in links]

    price=raw.find_all(["span"],{"class":["a-price-whole","a-price-fraction"]})
    price=[pt.get_text() for pt in price]

    #gathering main price and fraction of it
    price=[price[idx]+price[idx+1] for idx in range(0,len(price),2) ]

    name=raw.find_all(["span"],{"class":["a-text-normal"]})
    name=[pt.get_text() for pt in name]
    """
    
    #display the results
    print( 'name',len(name), 'price',len(price), 'links',len(links) )
    print("\nRESULTS for",i)
    decorate('==',40)
    for a,b,c in zip(name,price,links):
        print(" Name: {}\n      Price: {}\n            Link: www.amazon.com.tr{}".format( a, b, c ) )
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
