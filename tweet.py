#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import twitter
 
#USER_KEY = '6641182-8WT0NirJzNkRBx0pzWgEirVULgKxxKYcyKOgoD5lWa'
USER_KEY = '6641182-bvoTBWLgoU3HvsSkcvb7e7ZYjNoRxMBDjinlPSI'
#USER_SECRET = 'Kv4BaJUuGBzOieocs8HBj2ZLKwlkdEgwzR0ZnHu8y4s'
USER_SECRET = 'dRG2Ndlapcrv1V7Id78mIRqcAppScRePZxc3HBQKBk'
CONSUMER_KEY = 'a86KDAbgzutBDsv6axbmZw'
CONSUMER_SECRET = 'eGwZE2sptUP8qbgZa9rfLn3GDm5crONjw2v8pPvToM'
 
def get_oauth_keys():
    return USER_KEY, USER_SECRET, CONSUMER_KEY, CONSUMER_SECRET
 
user_key, user_secret, consumer_key, consumer_secret = get_oauth_keys()
 
api = twitter.Twitter(
    auth = twitter.OAuth(user_key, user_secret, consumer_key, consumer_secret))
 
kwargs = dict(
    screen_name='aomoriringo',
    count=10,
    page=1,
    include_entities=1,
    include_rts=1,
    exclude_replies=0)
 
#response = api.statuses.user_timeline(**kwargs)
 
#for stat in response:
#    print stat['text']
#    print(u'{created_at} {text}'.format(**stat))
 
mytext = u'from CentOS'
assert len(mytext) < 140
 
try:
    api.statuses.update(status=mytext)
except twitter.TwitterHTTPError as e:
    print e

