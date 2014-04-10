import webapp2
import logging
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
admin_template = os.path.join(os.path.dirname(__file__), 'admin.html')

class MainHandler(webapp2.RequestHandler):
  def get(self):
    order_by = self.request.get('order')
    stores = datamodel.Stores.all()
    stores.order('-deals_count')
    offers = datamodel.Offers.all()
    # offers.filter('expiry >=',datetime.date.today())
    
    if order_by=="popular":
      offers.order("-clicks")
    else:
      offers.order('-posted_on')
    offers.fetch(20)
    template_values = {
        'name': "Mahesh",'offers':offers,'stores':stores
      }
    self.response.out.write(template.render(path, template_values))
    
class SearchHandler(webapp2.RequestHandler):
  def get(self):
    try:
      query = str(self.request.get('q')).lower()
      stores = db.GqlQuery("SELECT * FROM Stores ORDER BY deals_count desc")
      where_clause = ""
      coupon_is_there = False
      if(query):
        for key in ["coupons","coupon"]:
          if key in query:
            where_clause = "WHERE offer_type='Coupon'"
            coupon_is_there = True
            query=query.replace(key,"")
        for key in ["deals","deal"]:
          if key in query:
            query=query.replace(key,"")
            where_clause = "WHERE offer_type='Deal'"
            if(coupon_is_there):
              where_clause=""
        for store in stores:
          key = store.store.lower()
          if key in query:
            query=query.replace(key,"")
            if where_clause!="":
              where_clause = where_clause + "and store='{0}'".format(store.store)
            else:
              where_clause = "WHERE store='{0}'".format(store.store)
      query_build= "SELECT * FROM Offers {0}".format(where_clause)
      offers = db.GqlQuery(query_build)
      offers_list = []
      for offer in offers:
        offers_list.append(offer)
      # sorted(offers_list,key=lambda k: k['posted_on'])
      self.response.write(offers_list[0])
      offers = offers_list
      data_query =[]
      if(query):
        query = ' '.join(query.split())
        for row in offers:
            if query in row.title.lower():
              data_query.append(row)
              offers = data_query
            elif query in row.description.lower():
              data_query.append(row)
              offers = data_query
      today = datetime.date.today()
      offers_desc = "All available offers for your query"
      # stores.append(db_stores)  # offers_list = [] # for offer in offers: #   offers_list.append(datetime.datetime.now() - offer.posted_on) # offers[offers.key].
      template_values = {
        'name': "Mahesh",'offers_desc':offers_desc,'offers':offers,'stores':stores,'today':today
      }# removed text: ,'offers_list':offers_list
      self.response.out.write(template.render(path, template_values))
    except Exception as exc:
        self.response.write("Exception:  ")
        self.response.write(exc)
        self.response.write("    Error at Line number:   ")
        self.response.write(sys.exc_traceback.tb_lineno)
        logging.error('There was an error in main form for query:'+self.request.get('q'))
        logging.error(exc)
        logging.error("At line number")
        logging.error(sys.exc_traceback.tb_lineno)
        
class Signin(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)

class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
      upload_url = blobstore.create_upload_url('/upload_photo')
      # self.response.write('<form method="post" action="'+upload_url+'"><input type="file"/><input type="submit" /></form>')
      self.response.out.write('<html><body>')
      self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
      self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
      name="submit" value="Submit"> </form></body></html>""")

      
    def post(self):
        try:
            upload = self.get_uploads()[0]
            t=upload.key()
            self.response.out.headers["Content-Type"]="application/json"
            output={'blob_key':str(t)}
            output=json.dumps(output)
            self.response.out.write(output)
            # self.redirect('/view_photo/%s' % upload.key())


        except Exception as exc:
            # self.redirect('/upload_failure.html')
            self.response.write("Exception")
            self.response.write(exc)

class PhotoServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    if not blobstore.get(resource):
            self.error(404)
    else:
            resource = str(urllib.unquote(resource))
            blob_info = blobstore.BlobInfo.get(resource)
            self.send_blob(blob_info)
    
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

class Contactus(webapp2.RequestHandler):
    def post(self):
        try:
            #self.response.write(current_row.author+users.get_current_user)
            name=self.request.get("contactus_name")
            description = self.request.get("contactus_desc")
            user=users.get_current_user()
            user_email = "test@test.com"
            if user:
                user_email=user.email()
                # self.response.write("1st your Query is successfully submitted"+name+":"+email+":"+description)
            
            email=self.request.get("contactus_email")
            new_data=datamodel.ContactUs(email=email,author=user_email,name=name,description=description)
            new_data.put()
            # self.response.write("Your Query is successfully submitted"+name+":"+email+":"+description)
            # self.redirect("/")
            self.response.write("Thank you for you contacting us.");
        except Exception, e:
            self.response.write(e)
            logging.error('There was an error in contact us:')
            logging.error(e)
            logging.error("At line number")
            logging.error(sys.exc_traceback.tb_lineno)

            # self.redirect("/")

            

app = webapp2.WSGIApplication([
  ('/', MainHandler),('/search', SearchHandler),('/signin',Signin),('/contactus',Contactus),('/upload_photo', PhotoUploadHandler),('/view_photo/([^/]+)?',PhotoServeHandler)
], debug=True)