import webapp2
import os
import datetime
import json
import urllib
import sys
#Custom imports
import datamodel

#Imports from Google Library
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.api import users

path = os.path.join(os.path.dirname(__file__), 'index.html')
stores_template = os.path.join(os.path.dirname(__file__), 'stores.html') 

offers = []
class OfferPage(webapp2.RequestHandler):
    def get(self):
      try:
        key=self.request.get('key')
        if offers_cache.len()==0:
          offers = datamodel.Offers.get(key)
        if key:
          self.response.out.headers['Content-Type']='text/json'
          offer = offers[0]
          dict={'link':str(offer.aff_link),'coupon':str(offer.coupon_code)}
          output=json.dumps(dict)
          offer.clicks =offer.clicks+1
          offer.put()
          self.response.out.write(output)
      except Exception as exc:
        self.response.write("Exception:")
        self.response.write(exc)

class StorePage(webapp2.RequestHandler):
    def get(self):
      user = users.get_current_user()
      try:
        if user:
          user_logged=user.nickname()
        else:
          user_logged = "Guest"
        stores = db.GqlQuery("SELECT * FROM Stores order by deals_count")
        if self.request.get("list"):
          # self.response.write("Inside the list page")
          template_values = {
            'name': user_logged,'stores':stores,'top_stores':stores[0:5]}
          self.response.out.write(template.render(stores_template, template_values))
          return
        store = self.request.get("store")
        type  = self.request.get("type")
        # self.response.write("No List of all stores")
        offers =  db.GqlQuery("SELECT * FROM Offers where store=:1 and enabled=True order by posted_on desc",store)  
        for me in stores:
          if me.store==store:
            me.clicks = me.clicks+1
            me.put()
        # today =  datetime.date.today()
        offers_desc = "All available offers from {0}".format(store)
        top_stores=[]
        for store in stores:
          top_stores.append(store)
        stores = top_stores
        template_values = {
            'name': "Mahesh",'offers_desc':offers_desc,'offers':offers,'stores':stores,'top_stores':stores[0:5]
        }
        self.response.out.write(template.render(path, template_values))
      except Exception as exc:
        self.response.write("Exception:")
        self.response.write(exc)
        self.response.write(sys.exc_traceback.tb_lineno)

app = webapp2.WSGIApplication([
  ('/offer',OfferPage), ('/store',StorePage),
], debug=True)