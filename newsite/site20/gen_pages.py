#
# Configuration...
#

PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGQwQ3lkazQ4akh2SDRwVXF5ck1ZWGc&output=csv"

#
# Library...
#
import common
import gen_subpages
import gen_movies
import gen_images
import gen_menus

def get_dct():
	items = common.parse_spreadsheet1( PAGE_DEF )
	dct = common.dct_join( items,'parent page key')
	return dct

def emitLine(f, str):
	f.write("%s\n" % str)	

def gen_page( page_name, page_def, movies_dct, images_dct, menus_dct ):
	accum_body = ""
	accum_style = ""	
	for item in page_def:
		asset_name = item["asset_name"]
		print "ASSET_NAME->", asset_name
		if asset_name.startswith("mov"):
			style, content = gen_movies.expand_item( item, movies_dct, images_dct )
		elif asset_name.startswith("img"):
			style, content = gen_images.expand_item( item, images_dct )
		elif asset_name.startswith("menu"):
			style, content = gen_menus.expand_item( item, images_dct, menus_dct )
		else:
			print "ERROR: Unknown asset type"
			sys.exit(1)
		accum_style += style
		accum_body += content

	fname = "%s_new.html" % page_name
	f = open( fname, 'w')
	f.write( "<html><body>" )
	f.write( accum_style )
	f.write( accum_body )
	f.write( "</body></html>" )
	f.flush()
	f.close()
	print "WROTE FILE->", fname

if __name__ == "__main__":
	dct = get_dct()
	print dct

	# get subpages...
	subpages_dct = gen_subpages.get_dct()
	print subpages_dct

	# get movies...
	movies_dct = gen_movies.get_dct()
	print movies_dct

	# get images...
	images_dct = gen_images.get_dct()
	print images_dct

	# get menus...
	menus_dct = gen_menus.get_dct()
	print menus_dct

	# iterate pages...
	for key in dct.keys():
		page_name = key
		page_def = []

		page_subpage_items = dct[key]
		for page_subpage_item in page_subpage_items:
			subpage_key = page_subpage_item['sub page key']
			subpage_items = subpages_dct[ subpage_key ]
			for subpage_item in subpage_items:
				page_def.append( subpage_item )
		
		gen_page( page_name, page_def, movies_dct, images_dct, menus_dct )
