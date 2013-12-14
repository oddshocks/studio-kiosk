import datetime
import os
import time

from flask import Flask, render_template
from twitter import *

app = Flask(__name__)

execfile("secrets.py")

@app.route("/")
def index():
    TWITTER_CREDS = os.path.expanduser('~/.twitter_creds')
    if not os.path.exists(TWITTER_CREDS):
        oauth_dance("studio-kiosk", CONSUMER_KEY,
                    CONSUMER_SECRET, TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(TWITTER_CREDS)

    twitter = Twitter(auth=OAuth(
                oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

    # usernames to get tweets for
    usernames = ["ashweedubz", "oddshocks", "iamHAYYLOVE", "mttalxndrgrrtt"]

    timelines = []

    for name in usernames:
        timelines.append(twitter.statuses.user_timeline(screen_name=name))

    catsfed = None
    now = datetime.datetime.now()
    with open('catsfed.txt') as f:
        catsfed = datetime.datetime.strptime(f.readline(), '%Y-%m-%d %H:%M:%S.%f')
    cats_last_fed = catsfed.strftime('%H:%M')
    hours_since_cats_fed = ('{0:.0f}').format(float((now - catsfed).seconds) / 60.0 / 60.0)

    return render_template("index.html", time=time, timelines=timelines,
                            cats_last_fed=cats_last_fed,
                            hours_since_cats_fed=hours_since_cats_fed)

@app.route("/feedcats")
def feedcats():

    with open('catsfed.txt', 'w') as f:
        f.write(str(datetime.datetime.now()))

    return render_template("feedcats.html")

if __name__ == "__main__":
    app.run(debug=True)
