import requests
from bs4 import BeautifulSoup

'''
some global stuff
'''
main_url = "https://solarmovie.pe/"
headers = {"user_agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}



links = []
names = []


def search(is_movie,name):
    '''
    function to search movies
    '''
    if len(name) > 1:
        name = name.replace(" ","-")
    
    search_url = main_url+"search/"+name
    
    
        
    r=requests.get(search_url,headers=headers)
        
    if r.status_code == 200:
        
        soup = BeautifulSoup(r.content,"lxml")
            
        flim_poster = soup.find_all("div",{"class":"film-poster"})
        
        if is_movie:
            '''
            if a movie
            '''
            
            for i in flim_poster:
                link = i.find("a")["href"]
                if "/movie/" in link:
                    links.append(str(link.split("-")[-1]))
                    names.append(str(i.find("a")["title"]))

            return links,names
        
        
        else:
            '''
            if a series
            '''
            for i in flim_poster:
                link = i.find("a")["href"]
                if '/tv/' in link:
                    links.append(str(link.split("-")[-1]))
                    names.append(str(i.find("a")["title"]))
            
            return links,names
                    
                    
            
def get_seasons(id):
    '''
    function to return no. of seasons and season ids
    '''
    
    season_url = f"{main_url}/ajax/v2/tv/seasons/{id}"
    r=requests.get(season_url,headers=headers)
    
    season_ids = [i['data-id'] for i in BeautifulSoup(r.text,'html.parser').select(".dropdown-item")]
    
    return season_ids
    

def get_episodes(id):
    '''
    function to return no. of episodes and episode ids
    '''
    
    episode_url = f"{main_url}/ajax/v2/season/episodes/{id}"
    r=requests.get(episode_url,headers=headers)
    
    episode_ids = [i['data-id'] for i in BeautifulSoup(r.text,'html.parser').select("a")]
    
    return episode_ids
    