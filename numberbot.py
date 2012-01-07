from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import httplib2
import simplejson
import oauth2
import twitter


class NumberBot(webapp.RequestHandler):
    
    def __init__(self):
        self.CONSUMER_KEY = 'buEIX2lNDgS9MJ0muaAEvQ'
        self.CONSUMER_SECRET = '3oK3WsyGEGH21yXWN9ns4tHrgKumZRo0TGZWRmcdWk'
        self.ACCESS_TOKEN_KEY = '77261630-4S9g2ScFlb82BIR7vqCnQHELHUT5gawAhuocwtCEe'
        self.ACCESS_TOKEN_SECRET = 'Yvpwld4J67zOzevqID3FSnI4uZOhCsLZqvI9Xcu4C0'
        self.ACCOUNT_NAME = "number_bot"
        self.PASSWORD = "numbers"

    # login (with OAuth authentication)
    def login(self):
        self.api = twitter.Api(cache=None,
                               consumer_key = self.CONSUMER_KEY,
                               consumer_secret = self.CONSUMER_SECRET,
                               access_token_key = self.ACCESS_TOKEN_KEY,
                               access_token_secret = self.ACCESS_TOKEN_SECRET)


    def get_allfriend_ids(self):        
        cursor = "-1"
        friend_ids = []
        
        while len( cursor ) > 1:
            json = self.api._FetchUrl("https://api.twitter.com/1/friends/ids.json?cursor=" + cursor + "&screen_name="
                                      + self.ACCOUNT_NAME)
            data = self.api._ParseAndCheckTwitter(json)
            friend_ids += data["ids"]
            cursor = data["next_cursor_str"]
            
        return friend_ids


    def get_allfollower_ids(self):
        cursor = "-1"
        follow_ids = []
        
        while len( cursor ) > 1:
            json = self.api._FetchUrl("https://api.twitter.com/1/followers/ids.json?cursor=" + cursor + "&screen_name="
                                      + self.ACCOUNT_NAME)        
            data = self.api._ParseAndCheckTwitter(json)
            follow_ids += data["ids"]
            cursor = data["next_cursor_str"]

        return follow_ids
    
    def modify_followers(self):
        followers = self.get_allfollower_ids()
        friends = self.get_allfriend_ids()
        
        followers_set = set(followers)
        friends_set = set(friends)

        self.response.out.write( len( followers_set ) )
        self.response.out.write( "\n\n" )
        self.response.out.write( len( friends_set ) )
        self.response.out.write( "\n\n" )
        
        #フォロー対象
        non_friends = followers_set - friends_set
                    
        #リムーブ対象
        bye_friends = friends_set - followers_set

        self.response.out.write( "follow -> ")
        self.response.out.write( len( non_friends ) )
        self.response.out.write( "\n\n remove -> " )
        self.response.out.write( len( bye_friends ) )


        for friend in bye_friends:
            try:
                self.api.DestroyFriendship(friend)
            except Exception, e:
                self.response.out.write( e.message )
                self.response.out.write( "\n" )
        
        for friend in non_friends:
            try:
                self.api.CreateFriendship(friend)
            except Exception, e:
                self.response.out.write( e.message )
                self.response.out.write( "\n" )
        
                  
    def get(self):
        
        # for test
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!\n')

        self.login()
        
        self.response.out.write( self.api.VerifyCredentials() )
        self.response.out.write( "\n" )

        # friends/followers同期
        self.modify_followers()
         
        #api.PostUpdate('test')
        

application = webapp.WSGIApplication([('/', NumberBot)], debug=True)    
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
