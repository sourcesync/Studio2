#
# Config...
#

CONTENT_KEY = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedExqa0xrZlpYbmtKWDhHOTVxWlFjS0E&output=csv"

WEBPAGE_TEMPLATE = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedEt1MnYxTk5lRzRZNXdXc05HRDlQTUE&output=csv"

WEBPAGE_ASSETS = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedG5SVzFyVVNaZUNXUi1BR0NqTkVwc2c&output=csv"

PHIL_WEBPAGE = "https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedFVhVGUySHBDbHZBd3RncXU0aGJNRnc&output=csv"

MOVIES_URL = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEtQS1ZvRVdRRTZZdTFCeDROdzVka2c&output=csv"

PHIL_PREFIX = "../phil_assets"

PAGES = [ 'e01' ]

DBG_NM = [ 'Pte111' ]

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
WEBPAGE_PHIL_DCT = {}
MOVIES_DCT = {}

# Func to read a spreadsheet and its schema...
def read_spreadsheet( url, pagetype=False ):
	response = urllib2.urlopen( url )
	data = response.read()
	lines = data.split("\n")
	# first line is schema...
	cols = lines[0].split(",")
	inds=range(len(cols))
	dct = {}
	items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >1 ]
	#for item in items:
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
        info[ item[1] ] = thisitem
        PAGE_DCT[key] = info
        if ( item[1] == 'cmary' ):
                pass


#
# Process the content key...
#
response = urllib2.urlopen( CONTENT_KEY )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >1 ]
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
		print "XYR->", key, xyreplace
	linkreplace = False
	if ( len(item)>8 ):
		linkreplace = item[8]
	click = False
	if len(item)>9 and item[9]!='':
		click = item[9]
		print "CLICK->", key, click
	thisitem = { 'item':item[1], 'exclude':exclude , 'xyr': xyreplace, 'linkr': linkreplace,'click':click }
	info[ item[1] ] = thisitem
	PAGE_DCT[key] = info
	if ( item[1] == 'cmary' ):
		pass

#PAGES = [ key for key in PAGE_DCT.keys() if key.strip()!='' ]
print "PAGES->",PAGES

#
# Process the webpage template...
#
response = urllib2.urlopen( WEBPAGE_TEMPLATE )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >=9 and line.split(",")[0].strip()!="" ]
for item in items:
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
	me = item[9].split(":")
	if len(me)<2: me = False
	mo = item[10].split(":")
	if len(mo)<2: mo = False
	info = { 'el':el, 'fp': os.path.join(parent,path), 'x':x, 'y':y, 'sel':sel, 'z':z, 'link':link, 'me':me, 'mo':mo }
        if WEBPAGE_TEMPLATE_DCT.has_key(nm):
		raise Exception('Key already exists')
	WEBPAGE_TEMPLATE_DCT[nm] = info

#
# Process the webpage assets...
#
response = urllib2.urlopen( WEBPAGE_ASSETS )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >=9 ]
for item in items:
	pid = item[0]
        el = item[1]
        nm = item[2]
	if nm.strip()=="": continue
        path = item[3]
        parent = item[4]
	# X,Y...
        x = item[5]
        y = item[6]
	# link...
	link = item[7]
	if link=='' or link=='0':
		link = False
	# Z...
	z = item[8]
	if z.strip()=='': z = 0
	# mouse enter/leave
	me = False
	mo = False
	if ( item[9] !=''):
		me = item[9].split(":")
		mo = item[10].split(":")	

        info = { 'el':el, 'fp': os.path.join(parent,path), 'x':x, 'y':y, 'z':z, 'link':link, 'me':me, 'mo':mo }

        if WEBPAGE_ASSETS_DCT.has_key(nm):
		print nm
                raise Exception('Key already exists ' + nm)
        WEBPAGE_ASSETS_DCT[nm] = info
	if False and nm=='c2m':
		sys.exit(0)

# PHIL WEB PAGE...
response = urllib2.urlopen( PHIL_WEBPAGE )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >=9 ]
if len(items)==0:
	print "ERROR: NOTHING IN PHIL WEBPAGE"
	sys.exit(1)
for item in items:
	el = item[1]
        nm = item[2]
	path = item[3]
	parent = item[4]
	x = item[5]
	y = item[6]
	link = item[7]
	z = item[8]

        # mouse enter/leave
        me = False
        mo = False
        if True and ( item[9] !=''):
                me = item[9].split(":")
                mo = item[10].split(":")
        info = { 'fp': os.path.join(parent,path), 'x':x, 'y':y, 'z':z, 'link':link, 'el':el, 'me':me, 'mo':mo }

        if WEBPAGE_PHIL_DCT.has_key(nm):
                info = WEBPAGE_PHIL_DCT[nm]
	WEBPAGE_PHIL_DCT[nm] = info	

def anim_script_item( anim, page_dct, srcid=None, prefix=None, otherdct=None):
	a = anim[0]
	b = anim[1]
	if (b=="show"):
		nm = a
		if page_dct.has_key(nm):
			info = page_dct[nm]
		else:
			info = otherdct[nm]

		fpath = info['fp']
		if prefix: fpath = os.path.join(prefix,fpath)	
		script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (nm,nm,fpath)
	elif ( b=="hide"):
		nm = a
                script = "document.getElementById('%s').style.visibility='hidden';" % nm
	elif ( b=="replace" ):
		nm = a
		info = page_dct[nm]
		fpath = info['fp']	
		if prefix: fpath = os.path.join(prefix,fpath)	
		script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (srcid,srcid,fpath)
		#print "REPLACE->", script
	return script

def mc_item( target, operation, src, dct, prefix=None):
	#print "mc_item->", target, operation, src, dct
	info = dct[src]
	fpath = info['fp']
	if prefix: fpath = os.path.join( prefix, fpath )
	script = "document.getElementById('%s').src='%s'" % (target,fpath)
	#print "mc script->", script
	return script	

# Process movies...
response = urllib2.urlopen( MOVIES_URL )
data = response.read()
lines = data.split("\n")
items = [ line.split(",") for line in lines[1:] if len(line.split(",")) >1 ]
for item in items:
	nm = item[0]
	if nm=='': continue
	path = item[1]
	parent = item[2]
	info = { 'fp':os.path.join(parent,path) }
	MOVIES_DCT[nm] = info
#print "movies->",MOVIES_DCT

#
# Func to emit an item...
#
def emit_item( page, DCT, item, PK=None, RDCT=None, PREFIX=None):
	#print "emit-item->", page, item
	if page in DBG_NM:
		print "DEBUG emit item->",page,item
	if item=='':
		print "ITEM IS EMPTY"
		return False
	if not DCT.has_key(item):
		print "WARNING: NO KEY->", item
		return False

	info = DCT[item]
	nm = item

	if nm in DBG_NM:
		print "DEBUG->", nm, info, (RDCT==None)

	# specify using page dct?...
	if ( info['x']=='x'):
		x = int(RDCT[PK][item]['xyr'][0])
	else:
		x = int(info['x'])

	if ( info['y'] == 'y' ):
		y = int(RDCT[PK][item]['xyr'][1])
	else:
		y = int(info['y'])

	# override using page dct?..
	if False and page == "test2" and RDCT:
		print "DEBUG->", page, item, RDCT[page][item]
	if RDCT and RDCT[page][item].has_key('xyr') and RDCT[page][item]['xyr']:
		x = int(RDCT[page][item]['xyr'][0])
		y = int(RDCT[page][item]['xyr'][1])

	# click info in page dct?...
	mc = ""
	if RDCT and RDCT[page][item].has_key('click') and RDCT[page][item]['click']:
		items = RDCT[page][item]['click'].split(":")
		mc = mc_item( items[0], items[1], items[2], DCT, PREFIX)
		#print "MCLICK->",mc

	if ( info['link'] == 'link' ):
		link = RDCT[PK][item]['linkr']
	else:
		link = info['link']

	# get z...
	if info['z']=='': info['z']= 0
	z = int(info['z'])

	# get path...
	fpath = info['fp']
	if PREFIX:
		fpath = os.path.join( PREFIX, fpath )

	link = info['link']

	# get animation info...
	me = False
	mo = False
	if info.has_key("me"):
		me = info["me"]
		mo = info["mo"]
	if nm in DBG_NM:
		print "DBG: emitem->",info, me, mo

	html = ""
	style = ""
	#html += "<style>\n"
        style += "#%s {\n" % nm
	style += "position: absolute;"
	style += "left: %dpx;\n" % x
	style += "top: %dpx;\n" % y
	style += "z-index: %d;\n" % z
	style += "overflow: hidden;\n"
	style += "border: 0px;\n"
	#html += "border: 1px dashed #333;"
	if info['el'] == 'imganim':
		style += "visibility: hidden;\n"	
        style += "}\n"
	style += "#%s.hover { border: 1px dashed #333; }\n" % nm
	#html += "</style>\n"


	# create the hover/out dhtml script...
	mover = ""
	mout = ""
	if me:
		mover = anim_script_item( me, DCT, nm, PREFIX )
	if mo:
		mout = anim_script_item( mo, DCT,nm, PREFIX )

	# emit the item...
	if info['el']=="imgmovie":
		minfo = MOVIES_DCT[ link ]
		mpath = minfo['fp']
		mpath = os.path.join("../phil_assets/",mpath)
		html += '<video controls id=%s poster="%s">' % (nm,fpath)
		html += '<source src="%s" />' % mpath
		html += '</video>'
	elif mc!="":
		html += '<img id=%s src="%s" ondragstart="DS=this;DSL=this.offsetLeft;DST=this.offsetTop;" ondrop="DODROP(event);" ondragover="this.className=\'hover\';return false" ondragenter="DT=this;DTL=this.offsetLeft;DTT=this.offsetTop;" ondragleave="this.className=\'\'" onmouseover="%s" onmouseout="%s" onclick="console.log(this);%s" />\n' % (nm,fpath,mover,mout,mc)
	elif link:
		html += '<a href="%s">' % (link+'.html')
		html += '<img id=%s src="%s" onmouseover="%s" onmouseout="%s"  />\n' % (nm,fpath,mover,mout)
		html += '</a>'
	elif nm=='gsbb':
		html += '<img id=%s src="%s" ondrop="alert(this);" ondragover="return false" ondragenter="alert(this);" />\n' % (nm,fpath)
	else:
		html += '<img id=%s src="%s" />\n' % (nm,fpath)

	if False and item=='c2m':
		#print item, info
		#print html
		sys.exit(0)

	return [ html, style ]

#
# Process desired pages...
#
counter = 15

for page in PAGES:
	style = ""
	html =  "<html>\n"
	html += "<head>\n"
	f = open("HEAD_SCRIPT.txt",'r')
	txt = f.read()
	f.close()
	html += txt
	html += "</head>\n"
	body = ""

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
					body += txt[0]
					style += txt[1]

		elif item.startswith("P"): # web page phil...
			if item.startswith("Ptj"): continue
			txt = emit_item( page, WEBPAGE_PHIL_DCT, item, page, PAGE_DCT, PHIL_PREFIX )
			body += txt[0]
			style += txt[1]
	
		else: # look in assets then in template...
			# search assets first...
			txt = emit_item( page,WEBPAGE_ASSETS_DCT, item, page, PAGE_DCT )
			if txt == False:
				# search template then
				txt = emit_item( page, WEBPAGE_TEMPLATE_DCT, item, page, PAGE_DCT )	
			body += txt[0]
			style += txt[1]

		if False and page == "e01":
			counter -= 1
			if counter <=0: 
				print "BREAK EARLY->", page, item
				break

	html += "<body>"
	html += "<style>"
	html += style
	html += "</style>"
	html += body
	html += "</body>"	
	html += "</html>\n"

	#print html

	f = open("%s.html" % page,'w')
	f.write( html )
	f.close()

