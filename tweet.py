#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
from tweepy import Stream, TweepError
import logging
import urllib
from seq import get_sequences
from token import (
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth_handler=auth)
seqs = get_sequences()

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tw_count = status.author.statuses_count
            s = seqs.search(tw_count)
            if s:
                sname = status.author.screen_name.encode('utf-8')
                print s.get_message(sname)
                api.update_status(s.get_message(sname), status.id)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', e
        return True          # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True          # Don't kill the stream

class UserStream(Stream):
    pass

def main():
    stream = UserStream(auth, CustomStreamListener())
    stream.timeout = None
    stream.userstream()

if __name__ == "__main__":
    main()
