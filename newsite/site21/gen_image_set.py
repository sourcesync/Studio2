#
#
# Configuration...
#

IMAGE_SET_DEFS = { "stbd_artists": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEFOWVdmZ2RFbVV4WWtUalNHN1RrcVE&output=csv" }

#
# Library...
#
import common
import os
import copy

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../videos"
VIDEOS_PREFIX = "../videos"
POSTERS_PREFIX = "../posters"

def expand_def( dct, item_def ):

	asset_name = item_def['asset_name']
	
	deff = dct[ asset_name ][0]
	
	path = deff["path"]
	filename = deff["filename"]

	fidx = filename.find("[")
	eidx = filename.find("]")

	regexpr = filename[0:fidx] + "%02d" + filename[eidx+1:]	

	seg = filename[fidx+1:eidx]
	parts = seg.split("-")

	start = int( parts[0] )
	end = int( parts[1] )

	asset_defs = []
	for i in range(start,end+1):
		ad = copy.deepcopy( item_def )
		ad['path'] = path
		ad['filename'] = regexpr % i
		ad['page_name'] = ad['filename'].split(".")[0]
		ad['asset_name'] = ad['page_name']
		ad['type'] = 'image_set'

		asset_defs.append( ad )
	
	return asset_defs

def get_attr( prop, asset_name, asset_def, default=None):
	if asset_def.has_key(prop):
		return asset_def[prop]
	else:
		return False

def expand_item( accum_ids, asset_def, is_dct, onclick=None, init_vis=None, ahref=None ):
	print "IMAGE SET EXPAND"

	# get the asset definition...
        asset_name = asset_def["asset_name"]
        item_def = asset_def

	# get id...
        htmlid = common.get_id(asset_name,accum_ids)
	accum_ids.append( htmlid )

	# get basic properties...
        image_path = get_item_path( asset_name, item_def )
        x = get_attr( 'x', asset_name, asset_def )
        y = get_attr( 'y', asset_name, asset_def )
        z = get_attr( 'z', asset_name, asset_def,'0')

	# init vis param override...
	init = get_attr( 'init', asset_name, asset_def)
	if init and not init_vis:
		init_vis = init

	# mouseover...
	mouseover = get_attr( 'mouseover', asset_name, asset_def )
	onmouseover = ""
	if mouseover:
		onmouseover = mouse_script_item( htmlid, mouseover )

	# mouseout...
	mouseout = get_attr( 'mouseout', asset_name, asset_def )
	onmouseout = ""	
	if mouseout:
		onmouseout = mouse_script_item( htmlid, mouseout )

	# onclick param override...
	#click = get_attr('click', asset_name, asset_def, '')
	#if click!='' and onclick==None:
	#parts = click.split(":")
	#onclick = click_script_item(parts[0], parts[1], parts[2], is_dct )
	
	# style...
	style  = ""
        style += common.emit_line( "#%s {" % htmlid )
        style += common.emit_line( "position: absolute;")
        style += common.emit_line( "left: %dpx;" % int(x) )
        style += common.emit_line( "top: %dpx;" % int(y) )
        style += common.emit_line( "z-index: %d;" % int(z) )
	if init_vis!=None:
		if init_vis:
        		style += common.emit_line( "visibility: %s;" % init_vis  )
		else:
        		style += common.emit_line( "visibility: %s;" % init_vis )
        style += common.emit_line( "}" )

	# content...
	content = ""

	# a href...
	if ahref:
		content += common.emit_line("<a href=%s >\n" % ahref )
	#else:
	#content += common.emit_line("<a href=# >\n"  )
		
	# onclick script...
	if onclick:
		content += common.emit_line( "<img id=%s src=\"%s\" onclick=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" >" % \
			(htmlid,image_path, onclick, onmouseover, onmouseout) )
	else:
		content += common.emit_line( "<img id=%s src=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" >" % \
			(htmlid,image_path, onmouseover, onmouseout ) )

	# end a href...	
	if ahref:
		content += common.emit_line("</a>\n" )
	#else:
	#content += common.emit_line("</a>\n" )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )
	scriptlet_dct['off']  = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'hidden' )
	if init_vis!=None:
		scriptlet_dct['init'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, init_vis)

        return [ style, content, "", scriptlet_dct ]

def get_item_path( name, item_def ):
        path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("PHIL",PHIL_PREFIX)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        fpath = fpath.replace("VIDEOS",VIDEOS_PREFIX)
        fpath = fpath.replace("VPOSTERS",POSTERS_PREFIX)
        return fpath

def get_dct( pagekeys=None ):
	if pagekeys==None:
		pagekeys = IMAGES_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not IMAGE_SET_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( IMAGE_SET_DEFS[code], "image set %s" % code )
		dct = common.dct_join( items,'name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
