'''
function to get server id and rabbit stream links
'''


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
    
    else:
        
        #for series
        url = f"https://solarmovie.pe/ajax/v2/episode/servers/{id}/#servers-list"
        
        r=requests.get(url,headers=headers)
        
        if r.status_code == 200:
            '''
            pick up the first server id
            '''
            soup = BeautifulSoup(r.text,'html.parser')
            sid = [i['data-id'] for i in soup.select('.link-item')][0]
            
            #generate rabbit link
            r = requests.get(f"https://solarmovie.pe/ajax/get_link/{sid}",headers=headers)
            return r.json()["link"]

def get_final_links(link):
    '''
    function to get final links
    '''
    languages = []
    subtitles = []
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
    
    '''
    subtitle part
    '''
    languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]        
    subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
    '''
    final link part
    '''
    final_link = x["sources"][0]["file"]
    
    qualities,links = get_m3u8_quality(final_link)
    
    return  languages,subtitles,qualities,links

