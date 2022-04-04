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

#set mpv executable
mpv_executable = "mpv.exe" if os.name == "nt" else "mpv"

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

#function to stream movie
def stream_movie(link,name):
    clear()
    colored_print("[*]Streaming: "+name)
    
    command = ' "'+link+'"'
    os.system(mpv_executable+command)
    
     
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
    qualities,links = get_final_links(link)
    f_link = select_quality(qualities,links)
    
    clear()
    colored_print('[S]tream Episode')
    colored_print('[D]ownload Episode')
    x = input("[*]Enter your choice: ")
    
    if  x == 'd' or x == 'D':
        pass
    else:
        stream_movie(f_link,names[i-1])
        
     
    
main()