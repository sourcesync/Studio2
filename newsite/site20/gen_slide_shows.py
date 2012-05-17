#
#
# Configuration...
#

SLIDE_SHOW_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGluSVVuQmpBUEhiQnV4REtxOEVSVWc&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"


#
# Library...
#
import common
import os
import gen_images

def expand_item( asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct, slide_shows_dct ):

        print "asset_def->", asset_def
        asset_name = asset_def["asset_name"]
        item_def = slide_shows_dct[asset_name]
        print "item_def->", item_def

	# create page scripts...
	script_dct = {}
	for pagekey1 in item_def.keys():
		script = ""
		dopage = 1
		for pagekey2 in item_def.keys():
			divname = "%s_%d" % ( asset_name, dopage )
			if pagekey1 == pagekey2:
				script += "document.getElementById('%s').style.visibility='visible';" % divname
			else:
				script += "document.getElementById('%s').style.visibility='hidden';" % divname
			dopage += 1
		script_dct[pagekey1] = script

	tot_style = ""
	tot_content = ""
	dopage=1
	while (True):
		if not item_def.has_key( str(dopage) ):
			break
	
		divname = "%s_%d" % ( asset_name, dopage )

		style  = common.emit_line("<style>")
		style += common.emit_line("#%s {" % divname )
		style += common.emit_line(" top:0px;")
		style += common.emit_line(" left:0px;")
		if dopage==1:
			style += common.emit_line(" visibility:visible;")
		else:
			style += common.emit_line(" visibility:hidden;")
		style += common.emit_line("}")
		style += common.emit_line("</style>")
		tot_style += style

		tot_content  += common.emit_line("<div id=%s >" % divname)
		
		pagedef = item_def[str(dopage)]
		print "pagedef->", pagedef

		for page_item in pagedef:
			print "page item->", page_item
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
				print "SCRIPT!!", script
	
				style, content = gen_images.expand_item( page_item, images_dct, script)
				tot_style += style
				tot_content += content

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

def get_dct():
	items = common.parse_spreadsheet1( SLIDE_SHOW_DEF )
	dct = common.dct_join( items,'name','page')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct
