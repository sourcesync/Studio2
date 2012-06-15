#
# Configuration...
#

CLICK_PANEL_DEFS = { "photos":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedEFLTGNNcHNhNmRCWHljUzlzN01SZ2c&output=csv" }

#
# Library...
#
import common
import os
import gen_images
import sys

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
	

def expand_item( accum_ids, asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct ):
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
