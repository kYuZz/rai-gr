#!/usr/bin/python

import urllib2
import BeautifulSoup
import mechanize
import os
import sys

MEDIA_PLAYER = 'mplayer'

if len(sys.argv) != 2:
	print 'Errore: devi specificare quale giornare radio vuoi ascoltare.'
	sys.exit(1)
gr = int(sys.argv[1])
if gr < 0 or gr > 3:
	print 'Errore: puoi scegliere solamente tra GR1, GR2 e GR3.'
	sys.exit(1)

BASE_URL = 'http://www.grr.rai.it' # NO trailing slash

br = mechanize.Browser()
print 'Opening URL %s...' % BASE_URL
response = br.open(BASE_URL)
body = response.read()
soup = BeautifulSoup.BeautifulSoup(body)
soup = BeautifulSoup.BeautifulSoup('%s' % soup.findAll('div', {'class': 'lancioRaitv'})[0])
gr_links = []
for i in soup.findAll('a'):
	for j in i.attrs:
		if j[0] == u'href':
			gr_links.append(BASE_URL + j[1])
gr_url = gr_links[gr - 1]

response = br.open(gr_url)
print 'Opening URL %s...' % gr_url
body = response.read()
soup = BeautifulSoup.BeautifulSoup(body)
for i in soup.findAll('script'):
	text = i.getText()
	if text.find('mediaUri') != -1:
		script_lines = text.split('\t')
		break
for i in script_lines:
	if i[0:8] == 'mediaUri':
		line = i
url = line.split("'")[1]

print 'Opening URL %s...' % url
f = urllib2.urlopen(url)
r = f.readlines()
f.close()

url = r[0]

if url[-4:] == '.mp3':
    print 'Stream URL found! %s' % url
    print 'Playing media...'
    cmd = '%s "%s"' % (MEDIA_PLAYER, url)
    os.system(cmd)
else:
    print 'ERROR: Stream URL non found!'



