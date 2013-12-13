import os

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

    return render_template("index.html", twitter=twitter)

if __name__ == "__main__":
    app.run(debug=True)
