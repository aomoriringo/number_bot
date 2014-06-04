#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
from tweepy import Stream, TweepError
from tweepy.models import Status
from tweepy.utils import import_simplejson
import logging
import urllib
from seq import get_sequences
from token import (
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

json = import_simplejson()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth_handler=auth)
seqs = get_sequences()
count = 0

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(CustomStreamListener, self).__init__(api)
        self.count = 0

    def on_data(self, raw_data):
        data = json.loads(raw_data)

        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, data)
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False
        elif 'direct_message' in data:
            status = Status.parse(self.api, data)
            if self.on_direct_message(status) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False
        elif 'friends' in data:
            pass # ignore
        else:
            logging.error("Unknown message type: " + str(raw_data))

    def on_status(self, status):
        try:
            self.count += 1
            tw_count = status.author.statuses_count
            s = seqs.search(tw_count)
            sys.stdout.write('\r%8s %-15s ' \
                             % (self.count, status.author.screen_name))
            sys.stdout.flush()
            if s:
                sname = status.author.screen_name.encode('utf-8')
                print s.get_message(sname)
                api.update_status(s.get_message(sname), status.id)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e

    def on_event(self, status):
        print status.event

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
