# -*- coding: utf-8 -*-

import sys
from tweepy import StreamListener, TweepError
from tweepy.models import Status
from tweepy.utils import import_simplejson
import logging
import urllib
from seq import get_sequences

json = import_simplejson()
seqs = get_sequences()

class CustomStreamListener(StreamListener):
    def __init__(self, api=None, options=None):
        super(CustomStreamListener, self).__init__(api)
        self.dry_run = options.dry_run
        self.verbose = options.verbose
        self.count = 0
        print 'start number_bot'

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if self.verbose:
            print data
            print '-'*60

        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, data)
            if self.on_status(status) is False:
                return False
        elif 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False
        elif 'friends' in data:
            pass # ignore
        else:
            logging.error("Unknown message type: " + str(raw_data))

    def on_status(self, status):
        if status.author.screen_name == 'number_bot':
            return True          # ignore
        try:
            self.count += 1
            tw_count = status.author.statuses_count
            s = seqs.search(tw_count)
            sys.stdout.write('\r%8s %-15s ' \
                             % (self.count, status.author.screen_name))
            sys.stdout.flush()
            if s:
                sname = status.author.screen_name.encode('utf-8')
                lang = status.author.lang
                message = s.get_message(sname, lang)
                print message
                if not self.dry_run:
                    self.api.update_status(message, status.id)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e

    def on_event(self, status):
        sid   = status.source['id']
        sname = status.source['screen_name']
        if sname == 'number_bot':
            pass             # ignore
        elif status.event == 'follow':
            if not self.dry_run:
                self.api.create_friendship(sid)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:' \
                 , status_code
        return True          # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True          # Don't kill the stream

