import os
import tweepy
import time
from secrets import *
from time import gmtime, strftime
from fn_shop import *


# ====== Individual bot configuration ==========================
bot_username = 'FNMasterBot'
logfile_name = bot_username + ".log"

# ==============================================================

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)


def create_tweet():
    """Create the text of the tweet you want to send."""
    # Replace this with your code!
    date = strftime("4:00pm PST, %B %d, %Y")
    text = "#Fortnite Shop Update at " + date + ". (fnbr.co/shop)\n\nSupport-A-Creator tag: FNMasterCom"
    # text = "Testing Twitter bot capability, tweet will be deleted almost immediately"
    create_shop(date)
    return text


def tweet(text):
    """Send out the text as a tweet."""

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def tweet_with_media(media, text):
    """Send a tweet with text and media"""

    # Send the tweet and log success or failure
    try:
        api.update_with_media(media, text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    for i in range(1, 10):
        print("slept for {0} seconds".format(i))
        time.sleep(1)
    tweet_text = create_tweet()
    tweet_with_media("daily_shop.png", tweet_text)
