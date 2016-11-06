# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2
import logging
import string
import cgi
import os
import re
import jinja2
import hmac
import random
import datetime
import hashlib
import json
import pprint
import time
import json

from google.appengine.ext import db
from google.appengine.api import memcache

SECRET = 'sdfsadfasdf;423!2fsd/fds'
DEBUG = True
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    print(os.path.join(os.path.dirname(__file__), 'templates'))
    t = jinja_env.get_template(template)
    return t.render(params)


class BlogHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_json(self, stringJson):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'   
        self.response.out.write(json.dumps(stringJson))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

def guests_key(group = 'default'):
    return db.Key.from_path('guests', group) # defines parent (works without it)

class Guest(db.Model):
    name = db.StringProperty(required = True)
    email = db.StringProperty() 
    events = db.StringProperty() 
    guest_ct = db.IntegerProperty()
    note = db.TextProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
        
class Register(BlogHandler):
    def post(self):
        print('imhere register')
        
        self.name = self.request.get("name")
        self.email = self.request.get("email")
        self.events = self.request.get("events")
        self.guest_ct = self.request.get("guest_ct")
        self.note = self.request.get("note")

        if not self.guest_ct:
            self.guest_ct = 0
        self.guest_ct = int(self.guest_ct)

        try:
            guest = Guest(parent = guests_key(), name = self.name, email = self.email, events = self.events, guest_ct = self.guest_ct, note = self.note)
            print('guest saved 1')
            guest.put()
            print('guest saved')

        except Exception, e:
            print '%s' % str(e)
            msg = "Authorization Failed. Please check if the credentials are correct"
            status = "error"

        else:
            msg = "Connected"
            status = "success"
        
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
            'msg': msg, 
            'status': status,
          } 
        self.response.out.write(json.dumps(obj))

class Main(BlogHandler):
    def get(self):
        #print('im1')
        self.render("onepage.html")


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/register', Register),
    ('/', Main)
    
                               ],
                              debug=DEBUG)


