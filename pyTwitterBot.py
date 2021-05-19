from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import tweepy
import random
import json
import matplotlib.pyplot as plt
import configparser
from values import *

def readConfig(key):
    parser = configparser.ConfigParser()
    parser.read("TwitterConfig.txt")
    return (parser.get("config", key))

def postTweet(text):
    #variables for accessing twitter API
    consumer_key=readConfig("consumer_key")
    consumer_secret_key=readConfig("consumer_secret_key")
    access_token=readConfig("access_token")
    access_token_secret=readConfig("access_token_secret")

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    tweet=text
    #Generate text tweet
    api.update_status(status=tweet, source = "")

def postArticolo():
    selectedSito = False
    selectedCategoria = False
    sitoScelto = ""
    categoriaScelta = ""

    while (not selectedSito):
        val = input("""Seleziona il sito:\n1) https://www.corriere.it/\n2) https://www.ilmessaggero.it/\n3) https://www.ilmattino.it/
4) https://www.passionepremier.com/\n5) https://www.passioneliga.com/\n>>>""")
        if(int(val) > 0 and int(val) < 6):
            print(sites[val])
            sitoScelto = sites[val]
            selectedSito = True
        else:
            print("Scelta non valida!!!\n")
    if(sites[val] != "https://www.passionepremier.com/" and sites[val] != "https://www.passioneliga.com/"):
        while (not selectedCategoria):
            val = input("Seleziona la categoria:\n1) Sport\n2) Economia\n3) Tecnologia\n>>>")
            if(int(val) > 0 and int(val) <= len(category)):
                print(category[val])
                categoriaScelta = category[val]
                selectedCategoria = True
                tag = tags[val]
            else:
                print("Scelta non valida!!!\n")

        print(sitoScelto + categoriaScelta + "/"    )
        html_page = urlopen(sitoScelto + categoriaScelta + "/")
        html_text = html_page.read()#.decode("utf-8")

        soup = BeautifulSoup(html_text, "html.parser")

        cont = 0

        linkArray = []

        for link in soup.find_all("a"):
            if(link.has_attr("href")):
                if(link["href"].endswith("html") and categoriaScelta+'/' in link["href"]):
                    cont = cont + 1
                    if(link["href"] not in linkArray):
                        pagina = link["href"]
                        if(sitoScelto not in link["href"] and "http" not in link["href"] and "www" not in link["href"]):
                            pagina = sitoScelto + link["href"]
                        if(link["href"].startswith("//")):
                            pagina = "https:" + link["href"]
                        linkArray.append(pagina)
            if(cont == 50):
                break
            
        titles = []
        links = []
        for link in linkArray:
            html_page = urlopen(link)
            html_text = html_page.read()
            soup = BeautifulSoup(html_text, "html.parser")
            for title in soup.find_all("h1"):
                if(title.text.strip() not in titles):
                    print(title.text.strip())
                    titles.append(title.text.strip())
                    links.append(link)

    else:
        html_page = urlopen(sitoScelto)
        html_text = html_page.read()

        soup = BeautifulSoup(html_text, "html.parser")

        cont = 0

        linkArray = []

        for link in soup.find_all("a"):
            if(link.has_attr("href")):
                if(link["href"].endswith("html")):
                    cont = cont + 1
                    if(link["href"] not in linkArray):
                        pagina = link["href"]
                        if(sitoScelto not in link["href"] and "http" not in link["href"] and "www" not in link["href"]):
                            pagina = sitoScelto + link["href"]
                        if(link["href"].startswith("//")):
                            pagina = "https:" + link["href"]
                        linkArray.append(pagina)
            if(cont == 50):
                break
        tag = tags['1']    
        titles = []
        links = []
        for link in linkArray:
            html_page = urlopen(link)
            html_text = html_page.read()

            soup = BeautifulSoup(html_text, "html.parser")
            for title in soup.find_all("h1"):
                if(title.text.strip() not in titles):
                    print(title.text.strip())
                    titles.append(title.text.strip())
                    links.append(link)
            
    randomNumber = random.randint(1, len(titles)-1)

    postTweet(titles[randomNumber] + "\n\n" + links[randomNumber] + "\n\n" +tag)

def postByWord(word):
    consumer_key=readConfig("consumer_key")
    consumer_secret_key=readConfig("consumer_secret_key")
    access_token=readConfig("access_token")
    access_token_secret=readConfig("access_token_secret")

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    new_tweets = api.search(q=word, count=20, result_type="mixed")
    tweetArray = []
    for tweet in new_tweets:
        id = tweet.id
        tweetArray.append(id)

    randomNumber = random.randint(1, len(tweetArray)-1)
    api.retweet(tweetArray[randomNumber])

def twitterTrends():
    consumer_key=readConfig("consumer_key")
    consumer_secret_key=readConfig("consumer_secret_key")
    access_token=readConfig("access_token")
    access_token_secret=readConfig("access_token_secret")

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    response = str(api.trends_place(718345))
    response = response[1:len(response)-1]
    response = response.replace("\'", "\"")
    response = response.replace("\"D\"", "\"D ")
    response = response.replace("None", "\"None\"")
    jsonObj = json.loads(response)

    names = []
    volumes = []
    for trend in jsonObj['trends']:
        if(trend["tweet_volume"] != "None" and int(trend["tweet_volume"]) > 30000 ):
            names.append(trend["name"])
            volumes.append(trend["tweet_volume"])

    zip_iterator = zip(names, volumes)
    a_dictionary = dict(zip_iterator)
    D = a_dictionary

    plt.bar(range(len(D)), list(D.values()), align='center', color='red', width=0.1)
    plt.xticks(range(len(D)), list(D.keys()))
    plt.title("Twitter Trends")
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()


#*****MAIN*****
primaScelta = False
while(not primaScelta):
    val = input("1) Posta Articolo\n2) Retwetta\n3) Visualizza Twitter Trends\n>>>")
    if(val == '1'):
        postArticolo()
        primaScelta = True
    elif (val == '2'):
        parola = input("Inserisci la parola che il tweet ritwittato deve contenere: ")
        postByWord(parola)
        primaScelta = True
    elif (val == '3'):
        twitterTrends()
        primaScelta = True

