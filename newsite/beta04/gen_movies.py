#
# Configuration...
#

#MOVIES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHFxcjk0RlA3RkxlaWdxdmIyZWJlM1E&output=csv"

MOVIES_DEFS = { "home": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGIwRUFBYWVabjN3amhvc2dXVTZDQWc&output=csv", \
		"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpsQWhEMi02UDJBeEl1S09uLTYxeEE&output=csv", \
		"animation_gallery":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHhXaDVyU3k0c1YtTXZ0Z0RJRG5wZ1E&output=csv",\
		"motiondesign_gallery":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedHYzLUxpQ2M5X0FaakFvZmVwSEcwQnc&output=csv", \
		"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFB5cFJiaEhIaF9lY0Q0cVg5Njl0clE&output=csv", \
		"interactive":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedE5xOGE0SlFwaWFmZS1DWnFPSWdsQ3c&output=csv", \
		"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFhpSHdRVm1VeFVpUHdhWjhYY0tlckE&output=csv" }

#
# Library...
#
import common
import os
import sys
import gen_images

VIMEO_EMBED = "embeds/vimeo.txt"

def get_dct(pagekeys=None):
	if pagekeys==None:
		pagekeys = MOVIES_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not MOVIES_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( MOVIES_DEFS[code], "movies %s" % code )
		dct = common.dct_join( items,'name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

def get_item_path( name, movies_dct ):
	item_def = movies_dct[name][0]
	path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = common.path_replace(fpath)
	return fpath


def expand_vimeo_item( accum_ids, asset_def, images_dct, movies_dct ):

	# get the movie asset name...
        asset_name = asset_def["asset_name"]

	# get the base def of the item...
        item_def = movies_dct[asset_name][0]

        # get an html id for video element...
        htmlid = common.get_id( asset_name, accum_ids )
        accum_ids.append(htmlid)

	# path is url...
	url = item_def["path"]

	# must have width and height...
	width = item_def['width']
	height = item_def['height']

        # get coords for def...
        x = int(asset_def['x'])
        y = int(asset_def['y'])
        z = asset_def['z']

	# content from template...
	f = open( VIMEO_EMBED, 'r')
	txt = f.read()
	f.close()
	content = txt.replace("URL",url)
	content = content.replace("HTMLID",htmlid)
	content = content.replace("WIDTH", width)
	content = content.replace("HEIGHT",height)
	content = content.replace("STYLE","position:absolute;visibility:inherit;top:%dpx;left:%dpx;z-index:4;" % (y,x) )
	
	# style...
	style = ""

	# dct...
        scriptlet_dct = {}
        #scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
        #scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % htmlid
        #scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
        
	scriptlet_dct['on'] = "document.getElementById('%s').setAttribute('src','%s?title=0&byline=0');" % (htmlid,url)
        scriptlet_dct['off'] = "document.getElementById('%s').setAttribute('src','');" % (htmlid)
        scriptlet_dct['init'] = "document.getElementById('%s').setAttribute('src','%s?title=0&byline=0');" % (htmlid,url)

        return [ style, content, scriptlet_dct ]

	
def expand_item( accum_ids, asset_def, images_dct, movies_dct ):

	print "mov->", movies_dct.keys()

	# get the movie asset name...
	asset_name = asset_def["asset_name"]

	# get the base def of the item...
	item_def = movies_dct[asset_name][0]

	# get type...
	typ = "file"
	if item_def.has_key("type"):
		typ = item_def["type"]

	# if video type, branch here...
	if typ == "vimeo":
		return expand_vimeo_item( accum_ids, asset_def, images_dct, movies_dct )

	# get the alt movie asset name, if any...
	alt_name = ""
	if asset_def.has_key("alt"): alt_name = asset_def["alt"]

	# get an html id for video element...	
	htmlid = common.get_id( asset_name, accum_ids )
	accum_ids.append(htmlid)

	# get the poster path, if any...
	poster_path = ""
	if item_def["poster"].strip()!="":
		poster = item_def["poster"].strip()
		poster_path = gen_images.get_item_path( poster, images_dct )
		poster_path = common.create_path( poster_path )

	# get the alternate movie path src, if any...
	alt_path = ""
	if alt_name != "":
		alt_path = get_item_path( alt_name, movies_dct )
		alt_path = common.create_path( alt_path )

	# finally, get the primary movie path src...
	movie_path = get_item_path( asset_name, movies_dct )
	movie_path = common.create_path( movie_path )

	# get coords for def...
	x = asset_def['x']
	y = asset_def['y']
	z = asset_def['z']

	# create the style...
	style  = ""
	style += common.emit_line( "#%s {" % htmlid )
	style += common.emit_line( "position: absolute;")
	style += common.emit_line( "left: %dpx;" % int(x) )
	style += common.emit_line( "top: %dpx;" % int(y) )
	style += common.emit_line( "z-index: %d;" % int(z) )
	style += common.emit_line( "visibility: hidden;" )
	style += common.emit_line( "}" )

	if poster_path == "":	
		content = common.emit_line( "<video controls id=%s ><source src=\"%s\" />CANNOT LOAD</video>" % (htmlid, movie_path) )
	else:
		if alt_path != "":
			content = common.emit_line( "<video controls id=%s poster=\"%s\" >" % ( htmlid, poster_path ) )
			content += common.emit_line( "<source src=\"%s\" />" % movie_path )
			content += common.emit_line( "<source src=\"%s\" />" % alt_path )
			content += common.emit_line( "</video>" )
		else:	
			content = common.emit_line( "<video controls id=%s poster=\"%s\" ><source src=\"%s\" /></video>" % (htmlid, poster_path, movie_path) )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
	scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % htmlid
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
	
	return [ style, content, scriptlet_dct ]

if __name__ == "__main__":
	dct = get_dct()
	print dct
