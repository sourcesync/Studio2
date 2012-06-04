#
# Configuration...
#

MOVIES_PANEL_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpERzFkdWxHMGpobXAzMHp3dkVNWkE&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os
import sys
import gen_movies

def get_dct():
	items = common.parse_spreadsheet1( MOVIES_PANEL_DEF )
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
	

def expand_item( accum_ids, page_item, images_dct, movies_dct, movie_panels_dct ):
	asset_name = page_item["asset_name"]
	item_def = movie_panels_dct[asset_name]

	tot_style = ""
	tot_content = ""

	htmlid = common.get_id( asset_name, accum_ids )
	accum_ids.append( htmlid )

	for item in item_def:
		print "MP ITEM->", item

		asn = item["asset_name"]
		if asn.startswith("mov"):
			style, content = gen_movies.expand_item( accum_ids, item, images_dct, movies_dct )
			tot_style += style
			tot_content += content

		else:
			print "ERROR: Cannot process->", item
			sys.exit(1)				
	return [ tot_style, tot_content ]

if __name__ == "__main__":
	dct = get_dct()
	print dct
