#
# Configuration...
#

CLICK_PANEL_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHFWblhXeHdlYllteXlnNVBTOE11R3c&output=csv"

#
# Library...
#
import common
import os
import gen_images

def get_dct():
	items = common.parse_spreadsheet1( CLICK_PANEL_DEF )
	dct = common.dct_join( items,'name')
	return dct

def get_item_path( name, movies_dct ):
	item_def = movies_dct[name][0]
	path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
	return fpath
	

def expand_item( asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct ):
	print "asset_def->", asset_def
	asset_name = asset_def["asset_name"]
	item_def = click_panels_dct[asset_name]
	print "CLICK PANELS, item_def->", item_def

	tot_style = ""
	tot_content = ""
	for item in item_def:
		asn = item["asset_name"]
		if asn.startswith("img"):
			style, content = gen_images.expand_item( item, images_dct )
			tot_style += style
			tot_content += content

	return [ tot_style, tot_content ]


if __name__ == "__main__":
	dct = get_dct()
	print dct
