#
#
# Configuration...
#

#IMAGES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFd0ZV81SS1yZmZqQnpGdVBUeTlvVEE&output=csv"

IMAGES_DEFS = { "home": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFJXcU9NdTFhcFV5MlU2dnpTODdjX2c&output=csv", \
	"whoweare":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEstNlZoTlN0WXhwbnR6VHpoSGc1Vmc&output=csv", \
	"sneakpeek":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHdlNS0wOHJ2Q1NzTjRsTF9XU25zSEE&output=csv", \
	"clients":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFRjOXdiRFJEazRadTh5ZFlIbk1CTVE&output=csv", \
	"contacts":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDN6d2xaYktMSlBCZnpqaXJGOEVnY0E&output=csv", \
	"community":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEVrOUcxQ3dkMlNzejVGdERYZ2tXb2c&output=csv", \
	"map":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHVRdFF4N0tfVmJTeXE0SFZNYUwxeVE&output=csv", \
	"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHNwVmwyMGRRT2xBWkJJcVd2MW93bnc&output=csv", \
	"photos":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDAwTzFCaHZpZDNaT0dPbmtldXdoUlE&output=csv", \
	"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHR0LV9KX2pHVnR2Y3BVMkl6c1NuU0E&output=csv", \
	"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGs5U3hqZkZ0VE1RblVTYTJrRndTZlE&output=csv", \
	#"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDRPby1XeDZHckd6bW1FcWZrcHFOM0E&output=csv", \
	"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDRPby1XeDZHckd6bW1FcWZrcHFOM0E&output=csv", \
	"motiondesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHJ1eUlfN2FNNFVDdnN2RVduOEFBNXc&output=csv", \
	"animation":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHlEV3RzRjJINmFpREo5SWtFajBvbGc&output=csv", \
	"animation_gallery":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdG9ncThyNTRrMXIwdGJnYkpDUzhVZ1E&output=csv", \
	"motiondesign_gallery":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedG5BenJiMzdGZzQyYmk4ZDh5SFllQ3c&output=csv", \
	"stbd_artists":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDBvU3pwSlJ0TEVfRFZteGxpUGQtSHc&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../videos"
VIDEOS_PREFIX = "../videos"
POSTERS_PREFIX = "../posters"
CAPTIONS_PREFIX = "../captions"
CONTENT_620 = "../content_6_20_2012"
CONTENT_625 = "../content_6_25_2012"

#
# Library...
#
import common
import os
import sys

def get_attr( prop, asset_name, asset_def, images_dct, default=None):
	if asset_def.has_key(prop):
		return asset_def[prop]
	else:
		item_def = images_dct[asset_name][0]
		if item_def.has_key(prop) and item_def[prop]!='':
        		val = item_def[prop]
			return val	
		elif default!=None:
			#print "WARNING: Returning default value->", default, prop, asset_name
			return default
		else:
			return False

def click_script_items( fieldstr ):
	scriptstr = ""	
	fields = fieldstr.split(":")
	for field in fields:	
                parts = click.split(":")
                onclick = click_script_item(parts[0], parts[1], parts[2], images_dct )
		scriptstr += onclick + ";"
	return scriptstr

def click_script_item( target, operation, src, images_dct ):
        info = images_dct[ src ][0]
        fpath = os.path.join( info['path'], info['filename'] )
	fpath = common.path_replace(fpath)
	fpath = common.create_path( fpath )
        script = "document.getElementById('%s').src='%s';document.getElementById('%s').style.visibility='visible';" % (target,fpath,target)
        return script

def mouse_script_item( srcid, val, images_dct ):
	anim = val.split(":")
        a = anim[0]
        b = anim[1]
        if (b=="show"):
                nm = a
                info = images_dct.has_key(nm)
                fpath = os.path.join( info['path'], info['filename'] )
		fpath = common.path_replace(fpath)
		fpath = common.get_path( fpath )
                script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (nm,nm,fpath)
		return script
        elif ( b=="hide"):
                nm = a
                script = "document.getElementById('%s').style.visibility='hidden';" % nm
		return script
        elif ( b=="replace" ):
                nm = a
                info = images_dct[nm][0]
                fpath = os.path.join( info['path'], info['filename'] )
		fpath = common.path_replace( fpath )
                script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (srcid,srcid,fpath)
        	return script
	else:
		print "WARNING: Nothing for mouse script item"
		return ""


def expand_item( accum_ids, asset_def, images_dct, onclick=None, init_vis=None, ahref=None, exturl=False ):
	print "IMAGE EXPAND"

	# get the asset definition...
        asset_name = asset_def["asset_name"]
        item_def = images_dct[asset_name][0]

	# get id...
        htmlid = common.get_id(asset_name,accum_ids)
	accum_ids.append( htmlid )

	# get basic properties...
        image_path = get_item_path( asset_name, images_dct )
        x = get_attr( 'x', asset_name, asset_def, images_dct )
        y = get_attr( 'y', asset_name, asset_def, images_dct )
        z = get_attr( 'z', asset_name, asset_def, images_dct,'0')

	# init vis param override...
	#init = get_attr( 'init', asset_name, asset_def, images_dct )
	#if init and not init_vis:
	#init_vis = init

	# mouseover...
	mouseover = get_attr( 'mouseover', asset_name, asset_def, images_dct )
	onmouseover = ""
	if mouseover:
		onmouseover = mouse_script_item( htmlid, mouseover, images_dct )

	# mouseout...
	mouseout = get_attr( 'mouseout', asset_name, asset_def, images_dct )
	onmouseout = ""	
	if mouseout:
		onmouseout = mouse_script_item( htmlid, mouseout, images_dct )

	# onclick param override...
	click = get_attr('click', asset_name, asset_def, images_dct, '')
	if click!='' and onclick==None:
		onclick = click_script_items( click )
		#parts = click.split(":")
		#onclick = click_script_item(parts[0], parts[1], parts[2], images_dct )

	# style...
	style  = ""
        style += common.emit_line( "#%s {" % htmlid )
        style += common.emit_line( "position: absolute;")
        style += common.emit_line( "left: %dpx;" % int(x) )
        style += common.emit_line( "top: %dpx;" % int(y) )
        style += common.emit_line( "z-index: %d;" % int(z) )
	style += common.emit_line( "border:none; " )
	style += common.emit_line( "visibility: hidden;")
	
	#if init_vis!=None:
	#if init_vis:
        #style += common.emit_line( "visibility: %s;" % init_vis  )
	#else:
        #style += common.emit_line( "visibility: %s;" % init_vis )
        style += common.emit_line( "}" )

	# content...
	content = ""

	# a href...
	if ahref:
		if exturl:
			content += common.emit_line("<a href=%s target=\"_blank\" >\n" % ahref )
		else:
			content += common.emit_line("<a href=%s >\n" % ahref )
	else:
		content += common.emit_line("<a href=# >\n"  )
		
	# onclick script...
	if onclick:
		content += common.emit_line( "<img id=\"%s\" src=\"%s\" onclick=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" alt=\"TheStudio\" >" % \
			(htmlid,image_path, onclick, onmouseover, onmouseout) )
	else:
		content += common.emit_line( "<img id=\"%s\" src=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" alt=\"TheStudio\" >" % \
			(htmlid,image_path, onmouseover, onmouseout ) )

	# end a href...	
	if ahref:
		content += common.emit_line("</a>\n" )
	else:
		content += common.emit_line("</a>\n" )

        if ( asset_name.find("caption_big") > 0 ):
                print "content->", content
                print "style->", style

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )
	scriptlet_dct['off']  = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'hidden' )
	#if init_vis!=None:
	#scriptlet_dct['init'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, init_vis)
	#else:
	scriptlet_dct['init'] =	"document.getElementById('%s').style.visibility = 'visible';" % (htmlid)

        return [ style, content, "", scriptlet_dct ]

def get_item_path( name, images_dct ):
	print "GIP->", name, images_dct.keys()
        item_def = images_dct[name][0]
	print "ID->", item_def
        path = item_def['path']
        fname = item_def['filename']
	print "PARTS->", path, fname
        fpath = os.path.join(path,fname)
        fpath = common.path_replace(fpath)
        return fpath

def get_dct( pagekeys=None ):
	if pagekeys==None:
		pagekeys = IMAGES_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not IMAGES_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( IMAGES_DEFS[code], "images->%s" % str(pagekeys) )
		dct = common.dct_join( items,'name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
