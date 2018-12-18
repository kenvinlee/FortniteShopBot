# FortniteShopBot
This is a twitter bot written in Python that tweets a daily Fortnite Shop image

The build uses the following libraries and APIs:
* tweepy
* Pillow
* fnbr.co's API

A small cheat is employed for the translucent background.

For those hoping to use this, there's a few things you'll need:
* Apply for fnbr.co and Twitter API access keys
* Put your API keys in a secrets.py file
* Unsure if the lack of the fonts used might cause a problem, but you might have to acquire the Burbank fonts

If you plug in your API keys and acquires the right fonts, you can most likely run a cron job to have the shop Tweeted every day. You might want to edit the shop image somewhat though.

The bot is meant for private use of the @FNMasterCom Twitter. This repo is to help others understand how to piece something like this together. Enjoy! 
