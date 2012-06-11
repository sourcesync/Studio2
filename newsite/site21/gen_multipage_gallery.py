#
#
# Configuration...
#

MPG_DEFS = { "animation_gallery": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGR5RGRySEhpenV1Z3ZocklGZTF3ekE&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"
VIDEOS_PREFIX = "../videos"

#
# Library...
#
import common
import os
import sys

import gen_movie_panels
import gen_movies
import gen_images

def get_attr( prop, asset_name, asset_def, images_dct, default=None):
	if asset_def.has_key(prop):
		return asset_def[prop]
	else:
		item_def = images_dct[asset_name][0]
		if item_def.has_key(prop) and item_def[prop]!='':
        		val = item_def[prop]
			return val	
		elif default!=None:
			print "WARNING: Returning default value->", default, prop, asset_name
			return default
		else:
			return False


def expand_item( accum_ids, asset_def, images_dct, onclick=None, init_vis=None, ahref=None ):

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
	init = get_attr( 'init', asset_name, asset_def, images_dct )
	if init and not init_vis:
		init_vis = init

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
		parts = click.split(":")
		onclick = click_script_item(parts[0], parts[1], parts[2], images_dct )

	
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

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )
	scriptlet_dct['off']  = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'hidden' )
	if init_vis!=None:
		scriptlet_dct['init'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, init_vis)

        return [ style, content, "", scriptlet_dct ]

def get_item_path( name, images_dct ):
        item_def = images_dct[name][0]
        path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("PHIL",PHIL_PREFIX)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        fpath = fpath.replace("VIDEOS",VIDEOS_PREFIX)
        return fpath

def gen_page( multipage_def, multipage_style, multipage_content, mp_dct, movies_dct, img_dct ):

	# iterate over pages...
	for page_def in multipage_def:

		accum_ids = []
	
		# intialize page style and content from template...
		tot_style = multipage_style
		tot_content = multipage_content

		# expand each asset...
		if page_def['asset_name'].startswith("mp"):
			style, content = gen_movie_panels.expand_item( accum_ids, page_def, img_dct, movies_dct, mp_dct )

			tot_style += style
			tot_content += content

		else:
			print "ERROR: Cannot process this asset type->", page_def
			sys.exit(1)




		# create all the html content...
                style = "<style>%s</style>" % (tot_style)
                content = tot_content
                head_script = "" #subpage_head_script
                load_script  = "" #subpage_load_script

		# get the page name...
		page_name = page_def['page_name']

                # write the file...
                common.gen_page( "%s.html" % page_name, style, content, head_script, load_script )


def gen_pages( multipage_style, multipage_content, mp_dct, movies_dct, img_dct ):
	mpgs_dct = get_dct()

	# iterate over all multipage sets ( or subset )...
	for key in mpgs_dct.keys():
		multipage_def = mpgs_dct[key]
		print "MULTIPAGE DCT->", multipage_def

		# generate the pages for this set...
		gen_page( multipage_def, multipage_style, multipage_content, mp_dct, movies_dct, img_dct )

def get_dct( pagekeys=None ):
	if pagekeys==None:
		pagekeys = MPG_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not MPG_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( MPG_DEFS[code] )
		dct = common.dct_join( items,'multipage_key')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
