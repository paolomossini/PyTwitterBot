# PyTwitterBot
PyTwitterBot is a TwitterBot written in Python. This project allows you to perform some interesting operations on a Twitter account such as: 
- Post articles from different websites
- Retweet using a key-word
- Generate a chart of Twitter trends

### Configuration
In order to configure the script you have to fill the TwitterConfig.txt file with the credentials of your Twitter application (previously created in your Twitter developer account):
```
consumer_key=
consumer_secret_key=
access_token=
access_token_secret=
```

### Scraping
In order to post articles from a website, the script performs a scraping of a page of the selected website, in order to extract all the latest articles published. Then the script chooses a random article to post on your Twitter account.

### External modules
- BeautifulSoup
- numpy 
- tweepy
- random
- json
- matplotlib.pyplot
- configparser

### Usage
#### Post Article
- Choose first action "Posta Articolo"
```
1) Posta Articolo
2) Retwetta
3) Visualizza Twitter Trends
>>>1
```
- Choose a website
```
Seleziona il sito:
1) https://www.corriere.it/
2) https://www.ilmessaggero.it/
3) https://www.ilmattino.it/
4) https://www.passionepremier.com/
5) https://www.passioneliga.com/
>>>
```
- Choose the category:
```
Seleziona la categoria:
1) Sport
2) Economia
3) Tecnologia
>>>
```

#### Retweet
- Choose second action "Retwetta"
```
1) Posta Articolo
2) Retwetta
3) Visualizza Twitter Trends
>>>2
```
- Insert the keyword:
`Inserisci la parola che il tweet ritwittato deve contenere: `

#### Generate Twitter trends chart
- Choose third action "Visualizza Twitter Trends"
```
1) Posta Articolo
2) Retwetta
3) Visualizza Twitter Trends
>>>3
```
