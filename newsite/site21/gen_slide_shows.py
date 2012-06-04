#
#
# Configuration...
#

SLIDE_SHOW_DEFS = { "whoweare": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEdJVkZzYkRNNF9vdllIVlFYYVFQVFE&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"


#
# Library...
#
import common
import os
import sys
import gen_images
import gen_movie_panels

def expand_item( accum_ids, asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct, slide_shows_dct ):

        asset_name = asset_def["asset_name"]
        item_def = slide_shows_dct[asset_name]

	# create page scripts...
	script_dct = {}
	for pagekey1 in item_def.keys():
		script = ""
		for pagekey2 in item_def.keys():
			divname = "%s_%d" % ( asset_name, int(pagekey2) )
			if pagekey1 == pagekey2:
				script += "document.getElementById('%s').style.visibility='visible';" % divname
			else:
				script += "document.getElementById('%s').style.visibility='hidden';" % divname
		script_dct[pagekey1] = script

	tot_style = ""
	tot_content = ""
	dopage=1
	while (True):
		if not item_def.has_key( str(dopage) ):
			break
	
		divname = common.get_id( "%s_%d" % ( asset_name, dopage ), accum_ids )
		accum_ids.append(divname)

		style  = ""
		#style  = common.emit_line("<style>")
		style += common.emit_line("#%s {" % divname )
		style += common.emit_line(" top:0px;")
		style += common.emit_line(" left:0px;")
		if dopage==1:
			style += common.emit_line(" visibility:visible;")
		else:
			style += common.emit_line(" visibility:hidden;")
		style += common.emit_line("}")
		#style += common.emit_line("</style>")
		tot_style += style

		tot_content  += common.emit_line("<div id=%s >" % divname)
		
		pagedef = item_def[str(dopage)]

		for page_item in pagedef:
			#print "SS page item->", page_item	
			page_asset_name = page_item["asset_name"]
	
			if ( page_asset_name.startswith("img") ):

				# determine script, if any...
				script = None
				if page_item.has_key("link") and page_item["link"]!="":
					link = page_item["link"]
					ltype,parm = link.split(":")
					if ltype=="page":
						script = script_dct[parm]	
					else:
						print "ERROR: unknown link type", ltype
						sys.exit(1)
	
				style, content = gen_images.expand_item( accum_ids, page_item, images_dct, script)
				tot_style += style
				tot_content += content

			elif ( page_asset_name.startswith("mp") ):
				
				style, content = gen_movie_panels.expand_item( accum_ids, page_item, images_dct, movies_dct, movie_panels_dct )
				tot_style += style
				tot_content += content
				

			else:
				print "ERROR: Cannot process->", page_item
				sys.exit(1)

		tot_content  += common.emit_line("</div>")

		dopage += 1

        return [ tot_style, tot_content ]

def get_item_path( name, images_dct ):
        item_def = images_dct[name][0]
        path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        return fpath

def get_dct(pagekeys=None):
	if pagekeys == None:
		pagekeys = SLIDE_SHOW_DEF.keys()
	newdct = {}
	for code in pagekeys:
		if ( not SLIDE_SHOW_DEFS.has_key(code) ): continue
		items = common.parse_spreadsheet1( SLIDE_SHOW_DEFS[code] )
		dct = common.dct_join( items,'name','page')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
