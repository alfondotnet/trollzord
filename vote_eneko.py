import mechanize
import cookielib
import sys

f = open("accounts.txt","r")
lines = f.readlines()
f.close()

num_votes = sys.argv[1]
accounts_vote = lines[0:int(num_votes)]

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
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


for acc in accounts_vote:

  br._ua_handlers['_cookies'].cookiejar.clear()

  r = br.open('http://rivals.redbull.com/es/login')
  html = r.read()

  br.select_form(nr=0)

  parts = acc.split(',')

  br.form['email'] = parts[0]
  br.form['password'] = parts[1]
  br.submit()

  print 'Voting...'

  r = br.open('http://rivals.redbull.com/es/frontuser/surfer_vote_this/182', "")

  # Here we would see if there is an error (such as max votes per ip)
  # and we would stop
  print r.read()

# # remove the first line
f = open("accounts.txt","w")
i = 0
for line in lines:
  i += 1
  if i <= (int(num_votes)):
    continue

  f.write(line)

f.close()
