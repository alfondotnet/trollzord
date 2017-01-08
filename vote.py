import mechanize
import cookielib
import urllib2
from sys import exit
import string
import json
from random import randint, choice
from time import sleep

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(choice(chars) for _ in range(size))

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

for i in xrange(1000):

  # clear cookies
  br._ua_handlers['_cookies'].cookiejar.clear()

  r = br.open('http://rivals.redbull.com/es/register')
  html = r.read()

  # <register-voter POST http://rivals.redbull.com/es/register application/x-www-form-urlencoded
  #   <HiddenControl(category=) (readonly)>
  #   <HiddenControl(team=) (readonly)>
  #   <TextControl(email=)>
  #   <PasswordControl(password=)>
  #   <PasswordControl(password_verify=)>
  #   <CheckboxControl(legal-check=[on])>>

  # Names
  fake_names = json.loads(urllib2.urlopen('http://api.namefake.com/spanish-spain/random/random').read())
  fake_emails = ['gmail.com', 'hotmail.com', 'aol.com', 'telefonica.es']
  pos_email = ['', str(randint(0, 124))]

  fake_name = fake_names['name']
  fake_tlfo = fake_names['phone_h']
  fake_email = fake_names['username'] + pos_email[randint(0,1)] + '@' + fake_emails[randint(0, len(fake_emails) - 1)]
  fake_password = id_generator(7)

  # Filling the register form
  br.select_form(nr=0)

  br.form['email'] = fake_email
  br.form['password'] = fake_password
  br.form['password_verify'] = fake_password

  br.submit()

  br.select_form(nr=0)

  namess = fake_name.split(' ')

  br.form['firstname'] = namess[0]
  br.form['lastname'] = namess[1]
  br.form['phone'] = fake_tlfo

  try:
    br.submit()
    # Log this thing
    acc_info = "\n" + fake_email + ',' + fake_password + ',' + fake_name.encode('utf-8') + ',' + fake_tlfo

    print 'Account created:'
    print "\t Acc info: " + acc_info

    with open('accounts.txt', 'a') as file_:
      file_.write(acc_info)
  except:
    pass
