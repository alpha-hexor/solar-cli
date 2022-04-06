'''
movie app cli
'''


import os
from termcolor import colored
import random
import sys
from codebase.search import *
from codebase.link_gen import *

#set ismovie
ismovie = True

#create download directory
if not os.path.exists('downloads'):
    os.mkdir('downloads')

#set mpv and ffmpeg executable
mpv_executable = "mpv.exe" if os.name == "nt" else "mpv"
ffmpeg_executable = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"

#clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#write a function to print colored text
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))

#function to select quality and send link
def select_quality(qualities,links):
    clear()
    colored_print("[*]Available Qualities: ")
    for i in range(len(qualities)):
        colored_print("["+str(i+1)+"] "+qualities[i])
    opt = int(input("[*]Enter index of the quality: "))
    return links[opt-1]

#function to select subtitles
def select_subs(languages,subtitles):
    if len(subtitles) == 0:
        return None
    else:
        clear()
        colored_print("[*]Available Subtitles: ")
        for i in range(len(subtitles)):
            colored_print("["+str(i+1)+"] "+languages[i])
        opt = int(input("[*]Enter index of the language: "))
        
        return subtitles[opt-1]

        

#function to stream movie
def stream_movie(link,sub_link,name):
    clear()
    colored_print("[*]Streaming: "+name)
     
    command = ' "'+link+'"' if sub_link == None else ' --sub-file="'+sub_link+'"'+' "'+link+'"'
    os.system(mpv_executable+command)

#function to download movie
def download_movie(path,link,sub_link,name):
    clear()
    
    if sub_link:
        colored_print("[*]Downloading Subtitles")
        r=requests.get(sub_link)
        with open(path+"\\subtitles.vtt","wb") as f:
            f.write(r.content)
        f.close()
        
    colored_print("[*]Downloading: " + name)
    command = f' -i "{link}" -c copy "{path}\\{name}.mp4"'
    os.system(ffmpeg_executable + command)
    
    
     
def main():
    query = input("Enter a movie name: ")
    links,names = search(ismovie,query)
    
    #display the results
    for i in range(len(names)):
        colored_print("["+str(i+1)+"] "+names[i])
        
    #get the user input
    i = int(input("Enter the number of the movie you want to watch: "))
    movie_to_watch = links[i-1]
  
    #rabbit link
    link = get_sid_link(ismovie,movie_to_watch)

    languages,subtitles,qualities,links = get_final_links(link)
    
    f_link = select_quality(qualities,links)
    
    sub_link = select_subs(languages,subtitles)
    
    clear()
    colored_print('[S]tream Episode')
    colored_print('[D]ownload Episode')
    x = input("[*]Enter your choice: ")
    
    if  x == 'd' or x == 'D':
        path = "downloads\\" + names[i-1].replace(" ","_").replace(":","")
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        download_movie(path,f_link,sub_link,names[i-1])
    else:
        stream_movie(f_link,sub_link,names[i-1])
        
     
    
main()