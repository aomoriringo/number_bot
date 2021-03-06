#!/usr/bin/env python
#-*- coding: utf-8 -*-

from optparse import OptionParser
from gettext import translation
from tweepy import Stream, API, OAuthHandler
from tweet import CustomStreamListener
from token import (
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

LANGUAGES=None

#def initialize_languages():
#    LANGUAGES = dict([(x, translation('number', languages=[x]) for x in ['ja']

def get_parser():
    parser = OptionParser()
    parser.add_option("-d", "--dry-run",
                      action="store_true",
                      dest="dry_run",
                      help="do not tweet", 
                      default=False) 
    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      help="verbose mode",
                      default=False)
    (options, args) = parser.parse_args()
    return (options, args)

def main():
    (options, args) = get_parser()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth_handler=auth)
    stream = Stream(auth, CustomStreamListener(api, options))
    stream.timeout = None
    stream.userstream()

if __name__ == "__main__":
    main()

