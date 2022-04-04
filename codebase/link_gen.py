'''
function to get server id and rabbit stream links
'''

from statistics import quantiles
import requests
from bs4 import BeautifulSoup
from .capctha import *
from .m3u8 import *

#some global shit
headers = {"user_agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

def get_sid_link(ismovie,id):
    '''
    function to get sid and rabbit stream link
    '''    
    if ismovie:
        url = "https://solarmovie.pe/ajax/movie/episodes/"+id
        
        r=requests.get(url,headers=headers)
        
        if r.status_code == 200:
            
            '''
            pick up the first server id
            '''
            soup = BeautifulSoup(r.content,'lxml')
            x=soup.find("li",attrs={"class":"nav-item"})
            
            sid = str(x.find("a")["data-linkid"])
            r = requests.get(f"https://solarmovie.pe/ajax/get_link/{sid}",headers=headers)
            return r.json()["link"]

def get_final_links(link):
    '''
    function to get final links
    '''
    
    qualities = []
    links = []
    
    #https://rabbitstream.net/embed-4/cGAGPSIA8PFI?z= --> cGAGPSIA8PFI
    
    rabbit_id = link.split("/")[-1].split("?")[0]
    
    r=requests.get(
        
        link,
        
        headers={
            "user_agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'referer' : "https://solarmovie.pe/"
        }
    )
    
    soup = BeautifulSoup(r.content,'html.parser')
    num = [i.text for i in soup.find_all("script")][-3].replace("var","")
    x=str(num).split(",")
    key=x[0].split("= ")[-1].replace("'","")
    times=x[1].split("= ")[-1].replace("'","")
    
    token = gettoken(key)
    
    x = req.get(f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbit_id}&_token={token}&_number={times}",headers={'user-agent':useragent,'X-Requested-With': 'XMLHttpRequest'}).json()
    
    
    final_link = x["sources"][0]["file"]
    
    qualities,links = get_m3u8_quality(final_link)
    
    return  qualities,links

