#
# Configuration...
#

CLICK_PANEL_OPTIONS_DEFS = { "photos":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedEtkUmFZbjE1YW90TkVOYWF1dVBneUE&output=csv", \
	"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFZ6RzRMWUtURWZOLUNjRUF6b3JocEE&output=csv" }

#
# Library...
#
import common
import os
import gen_images
import sys

def get_dct(pagekeys):
        if pagekeys==None:
                pagekeys = CLICK_PANEL_OPTIONS_DEFS.keys()
        newdct = {}
        for code in pagekeys:
                if not CLICK_PANEL_OPTIONS_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( CLICK_PANEL_OPTIONS_DEFS[code], "click panel options->%s" % str(pagekeys) )
		dct = common.dct_join( items,'name')
	return newdct

def get_item_path( name, movies_dct ):
	item_def = movies_dct[name][0]
	path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
	return fpath
	

def expand_item( accum_ids, asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct ):
	print "CLICK PANEL OPTIONS EXPAND->", asset_def["asset_name"], click_panels_dct.keys()

	asset_name = asset_def["asset_name"]
	item_def = click_panels_dct[asset_name]

	tot_style = ""
	tot_content = ""
	for item in item_def:
		asn = item["asset_name"]

		if asn.startswith("img"):
			style, content = gen_images.expand_item( accum_ids, item, images_dct )
			tot_style += style
			tot_content += content

		elif asn.startswith("mp"):
			style, content = gen_movie_panels.expand_item( accum_ids, item, images_dct )
			tot_style += style
			tot_content += content

		else:
			print "ERROR: Cannot process asset->", item
			sys.exit(0)

	return [ tot_style, tot_content ]


if __name__ == "__main__":
	dct = get_dct()
	print dct
