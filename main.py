#libraries used
import tweepy, requests, datanews, sqlite3
import datetime
from time import sleep

#api and access keys from twitter

API_KEY = "##############"
API_KEY_SECRET = "#######################"
ACCESS_KEY = "#############################"
ACCESS_KEY_SECRET = "##########################"

#global variables
title = ''
content = ''
url = ''
text = ''

def tweet():
    global text

    #using tweepy library to get access to account
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)

    #tweet with the text
    api = tweepy.API(auth)
    api.update_status(text)


def getting_text():
    global text, title, url, content

    repeated = True
    
    #getting the id number for the next tweet to be stored in database
    with open('twitterBot/output.txt', 'r') as f:
        idNum = int(f.readline())
        f.close()
    
    #connecting to database
    conn = sqlite3.connect('databases/twitter_bot.db')
    c = conn.cursor()
    
    #api key from datanews, and getting an article number
    datanews.api_key = '######################'
    articleNum = 0

    #connecting to datanews, and getting articles based on my preferences
    response = datanews.news(source = 'cnn.com', sortBy='relevance', language=['en'], from_date=str(datetime.date.today()))
    articles = response['hits'] 

    #fetching the title and url
    title = str(articles[articleNum]['title'])
    url = str(articles[articleNum]['url'])
    
    #checking if value is in the database
    c.execute("""select ids from Articles where headline = "{}" """.format(title))
    value = c.fetchone()

    #if not, it adds it to the database using the 
    if not value:
        c.execute("""insert into Articles(ids, headline) values ({}, "{}")""".format(idNum, title))
        conn.commit()
    
    else:

        #if it is in our database, it uses the list of articles we have already created,
        #  and goes thorugh finding one that hasn't been repeated 
        while articleNum < len(articles) - 1 and repeated == True:
            articleNum += 1

            title = str(articles[articleNum]['title'])
            url = str(articles[articleNum]['url'])

            c.execute("""select ids from Articles where headline = "{}" """.format(title))
            value = c.fetchone()

            if not value:
                repeated = False

        #if not repeated, then we found that hasn't been used yet
        if not repeated:
            c.execute("""insert into Articles(ids, headline) values ({}, "{}")""".format(idNum, title))
            conn.commit()
        else:
            
            #else, all articles have already been tweeted, and it returns false
            conn.close()
            return False
    
    #close connection with database
    conn.close()

    #change the id number for next article
    with open('twitterBot/output.txt', 'w') as f:
        f.write(str(idNum + 1))
        f.close()

     #getting the text for the tweet, and returning true   
    text = title + ' ' + url

    return True

#calling getting_text()
j = getting_text()

#if it return true, it tweets, else, it says 'No new news'
if j:
    tweet()
else:
    print("No new news.")

