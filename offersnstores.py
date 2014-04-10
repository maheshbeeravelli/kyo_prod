import webapp2
import os
import datetime
import json
import urllib

#Custom imports
import datamodel

#Imports from Google Library
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.api import users

path = os.path.join(os.path.dirname(__file__), 'index.html')

class OfferPage(webapp2.RequestHandler):
    def get(self):
      try:
        key=self.request.get('key')
        self.response.out.headers['Content-Type']='text/json'
        offer = datamodel.Offers.get(key)
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
        store = self.request.get("store")
        offers = db.GqlQuery("SELECT * FROM Offers where store=:1",store)
        stores = db.GqlQuery("SELECT * FROM Stores")
        for me in stores:
          if me.store==store:
            me.clicks = me.clicks+1
            me.put()
        # today =  datetime.date.today()
      
        template_values = {
          'name': user_logged,'offers':offers,'stores':stores
        } # Removed ,'today':today,'offers_list':offers_list
        self.response.out.write(template.render(path, template_values))
      except Exception as exc:
        self.response.write("Exception:")
        self.response.write(exc)


app = webapp2.WSGIApplication([
  ('/offer',OfferPage), ('/store',StorePage)
], debug=True)