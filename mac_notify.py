import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import logging
logging.basicConfig(filename='tweet.log',level=logging.INFO)

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
user_tweets = api.user_timeline()
curr_path = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(curr_path, 'twitter.png')


# The notifier function
def notify(title, subtitle, message, link):
    s = '-subtitle {!r}'.format('@'+subtitle)
    m = '-message {!r}'.format(message)
    l = '-open {!r}'.format(link)
    if link is not None:
        t = '-title {!r}'.format(title+' !!')
        command = 'terminal-notifier {}'.format(' '.join([m, t, s, l]))
    else:
        t = '-title {!r}'.format(title)
        command = 'terminal-notifier {}'.format(' '.join([m, t, s]))
    #logging.info("Command :%s" % command)
    os.system(command)


class MyListener(StreamListener):
    def on_status(self, status):
        link = None
        if hasattr(status, 'entities'):
            entities = status.entities
            if 'urls' in entities:
                urls = entities['urls']
                if len(urls) > 0:
                    url = urls[0]
                    if 'url' in url:
                        link = url['url'].encode('utf-8')
        user = status.user.name.encode('utf-8')
        text = status.text.encode('utf-8')
        logging.info("{}:{}:{}".format(user, text, link))
        notify(title='Twitter Notification',
               subtitle=user,
               message=text,
               link=link
               )

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.userstream(async=True)
