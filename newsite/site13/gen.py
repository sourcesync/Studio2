#
# Config...
#

CONTENT_KEY = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedExqa0xrZlpYbmtKWDhHOTVxWlFjS0E&output=csv"

WEBPAGE_TEMPLATE = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedEt1MnYxTk5lRzRZNXdXc05HRDlQTUE&output=csv"

WEBPAGE_ASSETS = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedG5SVzFyVVNaZUNXUi1BR0NqTkVwc2c&output=csv"

URL = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE9LamdZc0ZRbXVqTERsWjB1Ukg2WEE&output=csv"

PAGES = [ 'l01', 'c01','c02','c03','c04','c05','g01','b01','f01','f02','h01','i01','d01','d02','d03','d04' ]

DBG_NM = [  ]

#
# Program...
#
import urllib2
import os
import sys

# globals...
PAGE_DCT = {}
WEBPAGE_TEMPLATE_DCT = {}
WEBPAGE_ASSETS_DCT = {}

#
# Process the content key...
#
response = urllib2.urlopen( CONTENT_KEY )
data = response.read()
lines = data.split("\n")
#print lines
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >1 ]
#print items
for item in items:
	key = item[0]
	info = {}
	if PAGE_DCT.has_key(key):
		info = PAGE_DCT[key]
	exclude = False
	if ( len(item)>2) and ( item[2].strip()!="" ):
		exclude = [ item[2], item[3] ]
	xyreplace = False
	if ( len(item)>6 ) and item[6].strip()!="":
		xyreplace = [ int(item[6]), int(item[7]) ]
	link = False
	if ( len(item)>8 ):
		linkreplace = item[8]
	thisitem = { 'item':item[1], 'exclude':exclude , 'xyr': xyreplace, 'linkr': linkreplace }
	#print "THISITEM->", thisitem	
	info[ item[1] ] = thisitem
	#info.append( thisitem )
	PAGE_DCT[key] = info
	if ( item[1] == 'cmary' ):
		#print len(item), item
		#print thisitem
		#sys.exit(0)
		pass

#print PAGE_DCT

PAGES = [ key for key in PAGE_DCT.keys() if key.strip()!='' ]
print "PAGES->",PAGES

if DBG_NM:
	for item in DBG_NM:
		print "DEBUG PAGE->", item, PAGE_DCT[item]

#
# Process the webpage template...
#
response = urllib2.urlopen( WEBPAGE_TEMPLATE )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >=9 and line.split(",")[0].strip()!="" ]
for item in items:
	#print item
	el = item[0]
	nm = item[1]
	path = item[2]
	sel = int(item[3])
	parent = item[4]
	x = item[5]
	y = item[6]
	link = item[7]
        if link=='' or link=='0':
                link = False
	z = item[8]
	info = { 'el':el, 'fp': os.path.join(parent,path), 'x':x, 'y':y, 'sel':sel, 'z':z, 'link':link }
	#print info
        if WEBPAGE_TEMPLATE_DCT.has_key(nm):
		raise Exception('Key already exists')
	WEBPAGE_TEMPLATE_DCT[nm] = info
#print WEBPAGE_TEMPLATE_DCT

#
# Process the webpage assets...
#
response = urllib2.urlopen( WEBPAGE_ASSETS )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >=9 ]
for item in items:
        #print item
	pid = item[0]
        el = item[1]
        nm = item[2]
	if nm.strip()=="": continue
        path = item[3]
        parent = item[4]
        x = item[5]
        y = item[6]
	link = item[7]
	if link=='' or link=='0':
		link = False
	z = item[8]
	if z.strip()=='': z = 0
        info = { 'el':el, 'fp': os.path.join(parent,path), 'x':x, 'y':y, 'z':z, 'link':link }
        #print info
        if WEBPAGE_ASSETS_DCT.has_key(nm):
                raise Exception('Key already exists ' + nm)
        WEBPAGE_ASSETS_DCT[nm] = info
	#print nm, info
	if False and nm=='c2m':
		#print item
		sys.exit(0)
#print WEBPAGE_ASSETS_DCT

#
# Func to emit an item...
#
def emit_item( page, DCT, item, PK=None, RDCT=None ):
	print "emit-item->", page, item
	if page in DBG_NM:
		print "DEBUG emit item->",page,item
	if item=='':
		return False
	if not DCT.has_key(item):
		return False

	info = DCT[item]
	nm = item

	if ( info['x']=='x'):
		#print PK, item
		#print RDCT[PK][item]
		x = int(RDCT[PK][item]['xyr'][0])
	else:
		x = int(info['x'])

	if ( info['y'] == 'y' ):
		y = int(RDCT[PK][item]['xyr'][1])
	else:
		y = int(info['y'])


	if ( info['link'] == 'link' ):
		link = RDCT[PK][item]['linkr']
	else:
		link = info['link']

	z = int(info['z'])
	fpath = info['fp']
	link = info['link']

	html = ""
	html += "<style>\n"
        html += "#%s {\n" % nm
	html += "position: absolute;"
	html += "left: %dpx;\n" % x
	html += "top: %dpx;\n" % y
	html += "z-index: %d;\n" % z
        html += "}\n"
	html += "</style>\n"

	if link:
		html += '<a href="%s">' % (link+'.html')
		html += '<img id=%s src="%s" />\n' % (nm,fpath)
		html += '</a>'
	else:
		html += '<img id=%s src="%s" />\n' % (nm,fpath)

	if False and item=='c2m':
		#print item, info
		#print html
		sys.exit(0)

	return html

#
# Process desired pages...
#
for page in PAGES:
	html =  "<html>\n"
	html += "<head>\n"
	html += "</head>\n"
	html += "<body>\n"

	page_items = PAGE_DCT[page]
	for page_item_key in page_items.keys():
		page_item = page_items[page_item_key]
		item = page_item['item']
		if item=='': continue
		exclude = page_item['exclude']
		if item == 'temp':
			# iterate all assets...
			all_assets = WEBPAGE_TEMPLATE_DCT.keys()
			# add only the unsel ones...
			for asset in all_assets:
				#
				#possibly replace
				#
				override_sel = False
				if exclude and len(exclude)>0 and exclude[0]==asset:
					#print "EXCLUDE->", exclude, asset
					asset = exclude[1]
					override_sel = True
				info = WEBPAGE_TEMPLATE_DCT[asset]
				if info['sel']<1 or override_sel:
					txt = emit_item( page, WEBPAGE_TEMPLATE_DCT, asset )
					if txt == False: continue
					html += txt
					
		else:
			# search assets first...
			txt = emit_item( page,WEBPAGE_ASSETS_DCT, item, page, PAGE_DCT )
			if txt == False:
				# search template then
				txt = emit_item( page, WEBPAGE_TEMPLATE_DCT, item, None, None )	
			html += txt

	html += "</body>\n"
	html += "</html>\n"

	#print html

	f = open("%s.html" % page,'w')
	f.write( html )
	f.close()

