import requests

def get_m3u8_quality(link):
    links = []
    qualities = []
    
    
    r = requests.get(
        link,
        headers={
            'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
    )
    
    s=r.text.replace("#EXTM3U\n","").strip().split("\n")
    
    for i in range(0,len(s)-2+1,2):
        q=s[i].split(",")[-1].split("x")[-1] + "p"
        qualities.append(q)
        links.append(s[i+1]) 
        
    return qualities,links