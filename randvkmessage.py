#!/usr/bin/env python
import sys
import urllib2
import urllib
import cookielib
import mechanize
import BeautifulSoup
import re
import random
from time import sleep
import argparse
import time
import json

__version__ = 0.1
#CTRL+G -- go to line

USER_AGENT='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
PLAIN,JSON=0,1

class RandomVKMessage(object):
	'''try to authorization in vk or go to start'''
	'''login and password don't need it'''
	def __init__(self, login="",password="",decode='cp1251',wait=4,count=10):
		self.login = login
		self.password = password
		self.decode=decode
		self.wait=wait
		self.count = count
		if not isinstance(count,int):
			self.count = 4
		self.PLAIN=0
		self.JSON=1


		br = mechanize.Browser()
		self.br = br
		cookie = cookielib.CookieJar()
		br.set_cookiejar(cookie)

		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		br.addheaders = [('User-agent', USER_AGENT)]


		br.open('http://vk.com/')
		br.select_form(nr=0)
		br.form['email'] = login
		br.form['pass'] = password
		br.submit()
		response = br.response().read()
		if response.find("onLoginFailed") == -1:
			print "You're login in vk"
		else:
			print 'authorization is failed'


    #show results in plian text or in json format
	def show(self,id, name, message, format=PLAIN):
		def plain():
			return "id: %s\nname:%s\nmessage:%s\n" %(id, name, message)

		def mjson():
			return json.dumps({"id": id, "info":{"name":name, "message":message}})

		#maybe will be xml..

		arr = [('plain', plain),('json', mjson)]
		if format <= len(arr):
			print arr[format][1]()

	def start(self, format=PLAIN,element='wall_post_text'):
		if not isinstance(format,int):
			format=PLAIN
		print 'count: %d\nwait: %d\n' % (self.count, self.wait)
		t0=0
		while self.count != 0:
			st = self.read()
			if st != None:
				print  str(time.clock()- t0) + " seconds"
				self.show(st.get('id'), st.get('name'), st.get('message'),format)
				t0 = time.clock()
				self.count-=1

	#TO DO improve things around element
	def read(self,element='wall_post_text'):
		br = self.br
		#get random page id
		rand_id = random.randint(1,120000000)
		br.open('http://vk.com/id' + str(rand_id))
		storm = br.response().read().decode(self.decode)

		list_of_status = []
		soup = BeautifulSoup.BeautifulSoup(storm)
		for tag in soup.findAll('div', {"class": re.compile(element)}):
			if tag.string != None:list_of_status.append(tag.string)

		sleep(self.wait)
		if len(list_of_status) > 0:
			return dict({'message':list_of_status[random.randint(0, len(list_of_status)-1)], 
				         'name':soup.find(re.compile('title')).string, 
				         'id':str(rand_id)})



#Check valid email. If email not valid go out
#def valid_email(email):
    #return re.compile(r"^[\S]+@[\S]+\.[\S]+$").match(email)

#http://docs.python.org/library/argparse.html#module-argparse
#http://www.alexonlinux.com/pythons-optparse-for-human-beings


def main_parse():
	arg = sys.argv;
	parser = argparse.ArgumentParser()

	parser.add_argument('-v', action='store_const', dest='version',
                    const='vkstatus v%s' % __version__,
                    help='Store a constant value')
	parser.add_argument('--timeout', dest='timeout', help='timout for parse page. Recomment > 3s',default=3,type=int)
	parser.add_argument('--count', dest = 'count', help='number of iteration',default=10,type=int)
	parser.add_argument('--elem', dest='elem', help='default by wall_post_text')
	parser.add_argument('--login', dest='log', default=[""]*2, help='login, password')
	parser.add_argument('--decode', dest='decode', default='cp1251')
	parser.add_argument('--start', action='store_const', dest='constant_value',
                    const='value-to-store',
                    help='Store a constant value')
	parser.add_argument('--format', dest='format', help='export data in plain or json format')

	results = parser.parse_args()
	form=PLAIN
	if results.format != None and results.format.lower() == "json":
		form=JSON

	if results.version:
		print results.version
	elif len(arg) > 1:
		pass
		#app.run()
		'''message = RandomVKMessage(login=results.log[0], password=results.log[0], 
		decode=results.decode,wait=results.timeout, count=int(results.count))
		message.start(form)'''
	else:
		print parser.print_help()

if __name__ == '__main__':
	main_parse()



