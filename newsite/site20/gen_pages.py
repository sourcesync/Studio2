#
# Configuration...
#

PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGQwQ3lkazQ4akh2SDRwVXF5ck1ZWGc&output=csv"

SUBSET = ["c01"]

#
# Library...
#
import sys
import os
import common
import gen_subpages
import gen_movies
import gen_images
import gen_menus
import gen_movie_panels
import gen_click_panels
import gen_slide_shows

# old style...
import gen_templates
import gen_page_templates
import gen_template_assets

def get_dct():
	items = common.parse_spreadsheet1( PAGE_DEF )
	dct = common.dct_join( items,'parent page key')
	return dct

def emitLine(f, str):
	f.write("%s\n" % str)	

def gen_page( page_name, page_def, movies_dct, images_dct, menus_dct, movie_panels_dct, click_panels_dct, slide_shows_dct ):
	accum_ids = []
	accum_body = ""
	accum_style = ""	
	for item in page_def:
		asset_name = item["asset_name"]
		if asset_name.startswith("mov"):
			style, content = gen_movies.expand_item( item, movies_dct, images_dct )
		elif asset_name.startswith("img"):
			style, content = gen_images.expand_item( accum_ids, item, images_dct )
		elif asset_name.startswith("menu"):
			style, content = gen_menus.expand_item( item, images_dct, menus_dct )
		elif asset_name.startswith("cp"):
			style, content = gen_click_panels.expand_item( item, images_dct, movies_dct, movie_panels_dct, click_panels_dct )
		elif asset_name.startswith("ss"):
			style, content = gen_slide_shows.expand_item( accum_ids, item, images_dct, movies_dct, movie_panels_dct, click_panels_dct, slide_shows_dct )
		else:
			print "ERROR: Unknown asset type->", asset_name
			sys.exit(1)
		accum_style += style
		accum_body += content

	return accum_style, accum_body

if __name__ == "__main__":
	dct = get_dct()
	print dct

	# get subpages...
	subpages_dct = gen_subpages.get_dct()

	# get movies...
	movies_dct = gen_movies.get_dct()

	# get images...
	images_dct = gen_images.get_dct()

	# get menus...
	menus_dct = gen_menus.get_dct()

	# get click panels...
	click_panels_dct = gen_click_panels.get_dct()
	
	# get movie panels...
	movie_panels_dct = gen_movie_panels.get_dct()
	
	# get slide shows...
	slide_shows_dct = gen_slide_shows.get_dct()

	# get old template schema...
	template_dct = gen_templates.get_dct()

	# get old template assets...
	template_assets_dct = gen_template_assets.get_dct()

	# get old pages template dct..
	page_templates_dct = gen_page_templates.get_dct()

	# figure out which pages to render...
	if SUBSET and len(SUBSET)>0:
		pagekeys = SUBSET
	else:
		pagekeys = dct.keys()

	# iterate over all pages or subset...
	for page_name in pagekeys:

		# get the template based content...
		template_style, template_content = gen_page_templates.render_page( page_name, page_templates_dct, template_dct, template_assets_dct )
	
		# get the subpage items...	
		page_def = []
		page_subpage_items = dct[page_name]
		for page_subpage_item in page_subpage_items:
			subpage_key = page_subpage_item['sub page key']
			subpage_items = subpages_dct[ subpage_key ]
			for subpage_item in subpage_items:
				page_def.append( subpage_item )
	
		# generate the subpage content...	
		subpage_style, subpage_content = \
			gen_page( page_name, page_def, movies_dct, images_dct, menus_dct, movie_panels_dct, click_panels_dct, slide_shows_dct )

		# create all the html content...	
		style = "<style>%s</style>" % (template_style + subpage_style)
		content = template_content + subpage_content

		# write the file...
		common.gen_page( "%s.html" % page_name, style, content )
	
		
