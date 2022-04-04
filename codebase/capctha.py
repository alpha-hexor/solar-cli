from bs4 import BeautifulSoup
import requests as req
from bs4 import BeautifulSoup
import base64
import json

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

raw_domain = "https://rabbitstream.net:443"
domain = base64.b64encode(raw_domain.encode()).decode().replace("\n", "").replace("=", ".")


def gettoken(key):
    '''
    function to generate token
    '''
    
    r=req.get("https://www.google.com/recaptcha/api.js?render="+key,headers={'user-agent':useragent,'cacheTime':'0'})
    s=r.text.replace("/* PLEASE DO NOT COPY AND PASTE THIS CODE. */","")
    s=s.split(";")
    vtoken = s[10].replace("po.src=","").split("/")[-2]

    r=req.get("https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=cs3&k="+key+"&co="+domain+"&v="+vtoken,headers={'user-agent':useragent})
    
    soup = BeautifulSoup(r.content, "html.parser")
    recap_token = [i['value'] for i in soup.select("#recaptcha-token")][0]
    
    data = {
        "v" : vtoken,
        "k" : key,
        "c" : recap_token,
        "co" : domain,
        "sa" : "",
        "reason" :"q"
    }
    
    headers ={'user-agent':useragent,'cacheTime':'0'}
    
    j = json.loads(
        req.post("https://www.google.com/recaptcha/api2/reload?k="+key,data=data,headers=headers).text.replace(")]}'",'')
    )
    
    return j[1]