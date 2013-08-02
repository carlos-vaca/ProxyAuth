#Library Google


#Library System
import webapp2
import os
import jinja2
import re
import logging
import random
import string
import urllib
import json
import datetime
import cgi
import random
import string

import tweepy

from model.oauth import OAuthToken
from libs.sessions import *



FACEBOOK_APP_ID = "478630098854449"
FACEBOOK_APP_SECRET = "7f971e0e1add9922e9ee35b67f492d13"

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="1Mlqjen6DEBze6ysnAqmQ"
consumer_secret="vRhZQMjNJHC6Jzb36eICBlVCGckri8hVfdsfYeYkMJU"

class LoginHandler(BaseHandler):
    def get(self):
        '''auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        key = self.session.get('access_key')
        secret = self.session.get('access_secret')
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        name = api.me().name'''
        template_values = {
        'test':'name'
                }
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
        template = jinja_environment.get_template('/view/login.html')
        self.response.out.write(template.render(template_values))

class LoginFacebookHandler(BaseHandler):
    def get(self):
        client = cgi.escape(self.request.get('client'))
        callback = cgi.escape(self.request.get('callback'))
        if client == 'facebook':
            state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for x in xrange(32))
            args = dict(client_id=FACEBOOK_APP_ID, redirect_uri='http://localhost:8090/login/facebook?callback=facebook',state=state)
            self.redirect(
                "https://www.facebook.com/dialog/oauth?" +
            urllib.urlencode(args))
            return
        if callback == 'facebook':
            args = dict(client_id=FACEBOOK_APP_ID, redirect_uri='http://localhost:8090/login/facebook?callback=facebook')
            """redirect_url points to */login* URL of our app"""
            args["client_secret"] = FACEBOOK_APP_SECRET  #facebook APP Secret
            args["code"] = self.request.get("code")
            response = cgi.parse_qs(urllib.urlopen(
                "https://graph.facebook.com/oauth/access_token?" +
                urllib.urlencode(args)).read())
            access_token = response["access_token"][-1]
            profile = json.load(urllib.urlopen(
                "https://graph.facebook.com/me?" +
                urllib.urlencode(dict(access_token=access_token))))
            self.response.out.write(profile['name'])
            return

class LoginTwitterHandler(BaseHandler):
    def get(self):
        client = cgi.escape(self.request.get('client'))
        callback = cgi.escape(self.request.get('callback'))
        if client == 'twitter':
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'http://localhost:8090/login/twitter?callback=twitter')
            auth_url = auth.get_authorization_url()
            token_key = auth.request_token.key,
            token_secret = auth.request_token.secret
            self.session['token_key'] = auth.request_token.key
            self.session['token_secret'] = auth.request_token.secret
            self.redirect(auth_url)
        if callback == 'twitter':
            oauth_token = self.request.get("oauth_token", None)
            oauth_verifier = self.request.get("oauth_verifier", None)
            if oauth_token is None:
                # Invalid request!
                self.response.out.write('Error')
                return
            token_key = self.session.get('token_key')
            token_secret = self.session.get('token_secret')
            if token_key is None or token_secret is None:
                # We do not seem to have this request token, show an error.
                self.response.out.write('Error')
                return
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_request_token(token_key, token_secret)
            try:
                auth.get_access_token(oauth_verifier)
            except tweepy.TweepError, e:
                # Failed to get access token
                self.response.out.write('Error')
                return
            self.session['access_key'] = auth.access_token.key
            self.session['access_secret'] = auth.access_token.secret
            '''request_token.access_key = auth.access_token.key
            request_token.access_secret = auth.access_token.secret
            request_token.oauth_token = oauth_token
            request_token.oauth_verifier = oauth_verifier
            request_token.put()'''

            api = tweepy.API(auth)
            self.response.out.write(api.me().name)
        
        
        

app = webapp2.WSGIApplication([('/login', LoginHandler),
                               ('/login/facebook',LoginFacebookHandler),
                               ('/login/twitter', LoginTwitterHandler)],
                              debug=True, config=confighandler)

