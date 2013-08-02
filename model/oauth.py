#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright (C) 2009  pranny; pranny@gmail.com
#    
#    Initial work by JoshTheCoder 
#    at http://github.com/joshthecoder/tweepy/tree/master/examples/appengine/


from google.appengine.ext import db

class OAuthToken(db.Model):
    token_key = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)
    
    access_key = db.StringProperty()
    access_secret = db.StringProperty()
    
    oauth_token = db.StringProperty()
    oauth_verifier = db.StringProperty()
    
    when = db.DateTimeProperty(auto_now_add = True)