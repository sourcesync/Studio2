#
#
# Configuration...
#

MPG_SS_DEFS = { "stbd_artists": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEE2Tlo0YnpDREU2ZUdTNXdiU0Z1N2c&output=csv" }

PHIL_PREFIX = "../phil_assets"
VIDEOS_PREFIX = "../videos"

#
# Library...
#
import common
import os
import sys
import time

import gen_movie_panels
import gen_movies
import gen_images
import gen_image_set
import gen_embeds

#global
mpgs_dct = None

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
	style += common.emit_line( "visibility: hidden;" )
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
		content += common.emit_line("<a href=%s >\n" % ahref )

	# onclick script...
	if onclick:
		content += common.emit_line( "<img id=\"%s\" src=\"%s\" onclick=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" >" % \
			(htmlid,image_path, onclick, onmouseover, onmouseout) )
	else:
		content += common.emit_line( "<img id=\"%s\" src=\"%s\" onmouseover=\"%s\" onmouseout=\"%s\" >" % \
			(htmlid,image_path, onmouseover, onmouseout ) )

	# end a href...	
	if ahref:
		content += common.emit_line("</a>\n" )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )
	scriptlet_dct['off']  = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'hidden' )
	#if init_vis!=None:
	#scriptlet_dct['init'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, init_vis)

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

def get_link( item, is_dct, directive, page_name=None):
	global mpgs_dct

	print "GET LINK->", item, is_dct.keys()

	if mpgs_dct == None:
        	mpgs_dct = get_dct()
	print "MPGS DCT->", mpgs_dct.keys()
		
	link_name = item['link'].split(":")[0]
	print "LINK->",  link_name, mpgs_dct.keys()

	multipage_def = mpgs_dct[link_name]

        # find the is and the rest...
        is_def = None
        for page_def in multipage_def:
                if page_def['asset_name'].startswith("is"):
                        is_def = page_def
			break

        # expand the IS...
        asset_defs = gen_image_set.expand_def( is_dct, is_def )

	pages = [  asset['page_name'] for asset in asset_defs ]
	pages.sort()

	if directive == "first":
		return pages[0] + ".html"
	elif directive == "previous":
		print "ITEM->", item.keys(), page_name
		idx = pages.index( page_name ) -1
		if idx<0: idx = len(pages)-1
		return pages[idx] + ".html"
	elif directive == "next":
		print "ITEM->", item.keys(), page_name
		idx = pages.index( page_name ) + 1
		if idx>=len(pages): idx = 0
		return pages[idx] + ".html"
	else:
		print "ERROR: invalid directive->", directive
		sys.exit(1)

def gen_page_set( multipage_def, multipage_style, multipage_content, mp_dct, movies_dct, img_dct, is_dct, embeds_dct ):

	# find the is and the rest...
	is_def = None
	remaining_defs = []
	for page_def in multipage_def:
                if page_def['asset_name'].startswith("is"):
                        is_def = page_def
		else:
			remaining_defs.append( page_def )

	# expand the IS...
	asset_defs = gen_image_set.expand_def( is_dct, is_def )
	for asset in asset_defs:
			
		accum_ids = []

		# intialize page style and content from template...
		tot_style = multipage_style
		tot_content = multipage_content
		tot_on = ""
		tot_off = ""

		cur_page_name = asset['page_name']
		cur_asset_path = os.path.join( asset['path'], asset['filename'] )
		cur_asset_path = common.path_replace( cur_asset_path )
		print  cur_asset_path
	
		alldefs = remaining_defs + [ asset ]
		for page_def in alldefs:

                	# expand each asset...
                	if page_def['asset_name'].startswith("img"):
				# determine the script, if any...
                        	script = None
                        	ahref = None
				exturl = None

				print "MSS IMG DEF->", page_def
                        	if page_def.has_key("link") and page_def["link"]!="":
                                	link = page_def["link"]
					print "LINK PAGE DEF->", link, page_def.keys(), page_def['asset_name'], page_def['link']
                                	if link.startswith("option:"):
                                        	ltype,parm = link.split(":")
                                        	funcname = "func_%s_%s" % (menu_name, parm)
                                        	test = action_scripts[funcname]
                                        	script = "%s ();" % funcname
                                	elif link.startswith("url:"):
                                        	idx = link.find(":") + 1
                                        	ahref = link[idx:]
                                	elif link.startswith("nurl:"):
                                        	idx = link.find(":") + 1
                                        	ahref = link[idx:]
                                        	exturl = True
					elif link.startswith("mss"):
                                        	idx = link.find(":") + 1
						directive = link[idx:]
						ahref = get_link( page_def, is_dct, directive, cur_page_name )
						print "MS LINK->", ahref
                                	else:
                                        	print "ERROR: multipage_slide_show: Unknown link type", page_def
						sys.exit(1)

                        	style, content, foo, scriptlet_dct = gen_images.expand_item( accum_ids, page_def, img_dct, script, None, ahref, exturl )

                        	tot_style += style
                        	tot_content += content
				tot_on += scriptlet_dct["on"]
				tot_off += scriptlet_dct["off"]

			elif page_def.has_key('type') and page_def['type'] == "image_set":

				# Note, we are requiring a valid cap file...
                                if page_def.has_key('cap_file') and page_def['cap_file']!=None:
					print "WARNING: Got cap file->", page_def['cap_file']	
				else:	
					print "WARNING: No cap file->", page_def
					time.sleep(2)
					continue

				style, content, foo, scriptlet_dct = gen_image_set.expand_item( accum_ids, page_def, is_dct, None, None, None )
                        	tot_style += style
                        	tot_content += content
				tot_on += scriptlet_dct["on"]
				tot_off += scriptlet_dct["off"]

				# expand the caption too...
                                if page_def.has_key('cap_path'):
					style, content, foo, scriptlet_dct = \
						gen_image_set.expand_caption( accum_ids, page_def )
                                	tot_style += style
                                	tot_content += content
                                	tot_on += scriptlet_dct["on"]
                                	tot_off += scriptlet_dct["off"]

			elif page_def['asset_name'].startswith("embed"):

				print cur_page_name
				print page_def

				override_link = common.SITE + "/" + cur_page_name + ".html"
				override_image = common.SITE + "/" + cur_asset_path
				print override_link, override_image

				style, content, foo, scriptlet_dct = gen_embeds.expand_item( accum_ids, page_def, embeds_dct, img_dct, override_link, override_image )
                                tot_style += style
                                tot_content += content
                                tot_on += scriptlet_dct["on"]
                                tot_off += scriptlet_dct["off"]

			else:
				print "ERROR: gen_multipage_slideshow: Cannot process this asset type->", page_def
				sys.exit(1)

		# create all the html content...
		style = "%s" % (tot_style)
		content = tot_content
		head_script = "" #subpage_head_script
		load_script  = tot_on #subpage_load_script

		# get the page name...
		page_name = asset['page_name']

		# write the file...
		common.gen_page( "%s.html" % page_name, style, content, head_script, load_script )


def gen_pages( page_def, multipage_style, multipage_content, mp_dct, movies_dct, img_dct, is_dct, embed_dct ):
	asset_name = page_def['asset_name']

	mpgs_dct = get_dct()

	mpgs_items = mpgs_dct[asset_name]

	# generate the pages for this set...
	gen_page_set( mpgs_items, multipage_style, multipage_content, mp_dct, movies_dct, img_dct, is_dct, embed_dct )

def get_dct( pagekeys=None ):
	if pagekeys==None:
		pagekeys = MPG_SS_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not MPG_SS_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( MPG_SS_DEFS[code], "multipage slide show %s" % str(pagekeys))
		dct = common.dct_join( items,'multipage_key')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
