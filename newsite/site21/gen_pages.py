#
# Configuration...
#

PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGQwQ3lkazQ4akh2SDRwVXF5ck1ZWGc&output=csv"

SUBSET = [ "home","whoweare","sneakpeek","clients", "contacts" ,\
	"community", "map", "partners", "photos", "etcetera", "interactive", "animation", \
	"animation_gallery", "motiondesign","motiondesign_gallery" ]

SUBSET = [ "clients" ]

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
import gen_movies
import gen_movie_panels
import gen_click_panels
import gen_slide_shows
import gen_embeds
import gen_multipage_gallery

# old style...
import gen_templates
import gen_page_templates
import gen_template_assets

def get_dct():
	items = common.parse_spreadsheet1( PAGE_DEF , "pagedef" )
	dct = common.dct_join( items,'parent page key')
	return dct

def emitLine(f, str):
	f.write("%s\n" % str)	

def gen_page( accum_ids, page_name, page_def, movies_dct, images_dct, menus_dct, movie_panels_dct, click_panels_dct, slide_shows_dct, embeds_dct ):
	accum_body = ""
	accum_style = ""
	accum_script = ""	

	load_script = ""

	print "MAIN - GEN PAGE ITEMS->", [ a["asset_name"] for a in page_def ]

	for item in page_def:

		scriptlet_dct = {}
		script = ""

		asset_name = item["asset_name"]

		if asset_name.startswith("mov"):
			style, content = gen_movies.expand_item( accum_ids, item, images_dct, movies_dct )

		elif asset_name.startswith("img"):
			style, content, script, scriptlet_dct = gen_images.expand_item( accum_ids, item, images_dct )

		elif asset_name.startswith("embed"):
			style, content, script, scriptlet_dct = gen_embeds.expand_item( accum_ids, item, embeds_dct )

		elif asset_name.startswith("menu"):
			print "MAIN - CALLING GEN MENUS EXPAND", asset_name
			style, content, script, scriptlet_dct  = gen_menus.expand_item( accum_ids, item, images_dct, menus_dct, \
				slide_shows_dct, movies_dct, movie_panels_dct )

		elif asset_name.startswith("cp"):
			style, content = gen_click_panels.expand_item( accum_ids, item, images_dct, movies_dct, movie_panels_dct, click_panels_dct )

		elif asset_name.startswith("ss"):
			style, content, script, scriptlet_dct = \
				gen_slide_shows.expand_item( accum_ids, item, images_dct, movies_dct, movie_panels_dct, click_panels_dct, slide_shows_dct )

		else:
			print "ERROR: Unknown asset type->", asset_name
			sys.exit(1)

		accum_style += style
		accum_body += content
		accum_script += script

		# deal with page onload scripts...
		if scriptlet_dct.has_key("init"):
			load_script += scriptlet_dct['init']
		elif scriptlet_dct.has_key("on"):
			load_script += scriptlet_dct['on']

	return accum_style, accum_body, accum_script, load_script

if __name__ == "__main__":
	dct = get_dct()

        # figure out which pages to render...
        if SUBSET and len(SUBSET)>0:
                pagekeys = SUBSET
        else:
                pagekeys = dct.keys()

	# get subpages...
	subpages_dct = gen_subpages.get_dct( pagekeys )

	# get movies...
	movies_dct = gen_movies.get_dct( pagekeys )

	# get images...
	images_dct = gen_images.get_dct( pagekeys )

	# get images...
	embeds_dct = gen_embeds.get_dct( pagekeys )
	
	# get menus...
	menus_dct = gen_menus.get_dct( pagekeys )

	# get click panels...
	click_panels_dct = None #gen_click_panels.get_dct( pagekeys )
	
	# get movie panels...
	movie_panels_dct = gen_movie_panels.get_dct( pagekeys )
	
	# get slide shows...
	slide_shows_dct = gen_slide_shows.get_dct( pagekeys )

	# get old template schema...
	template_dct = gen_templates.get_dct()

	# get old template assets...
	template_assets_dct = gen_template_assets.get_dct()

	# get old pages template dct..
	page_templates_dct = gen_page_templates.get_dct( pagekeys )

	# iterate over all pages or subset...
	for page_name in pagekeys:

		# Restart the id namer...
		accum_ids = []

		# get the template based content...
		template_style, template_content = gen_page_templates.render_page( accum_ids, page_name, page_templates_dct, template_dct, template_assets_dct )

		# get the subpage items...	
		page_def = []
		page_subpage_items = dct[page_name]
		for page_subpage_item in page_subpage_items:
			subpage_key = page_subpage_item['sub page key']
			subpage_items = subpages_dct[ subpage_key ]
			for subpage_item in subpage_items:
				page_def.append( subpage_item )

		print "MAIN - PAGE DEF", page_name, dct, page_def

		if page_def[0]['asset_name'] == "mpg_animation_gallery":
			gen_multipage_gallery.gen_pages( page_def[0], template_style, template_content, movie_panels_dct, movies_dct, images_dct )
		
		elif page_def[0]['asset_name'] == "mpg_motiondesign_gallery":
			gen_multipage_gallery.gen_pages( page_def[0], template_style, template_content, movie_panels_dct, movies_dct, images_dct )

		else:

			print "MAIN - GENERATING PAGE FOR", page_name

			# generate the subpage content...	
			subpage_style, subpage_content, subpage_head_script, subpage_load_script = \
				gen_page( accum_ids, page_name, page_def, movies_dct, images_dct, menus_dct, movie_panels_dct, click_panels_dct, slide_shows_dct, embeds_dct )

			# create all the html content...	
			style = "<style>%s</style>" % (template_style + subpage_style)
			content = template_content + subpage_content
			head_script = subpage_head_script
			load_script  = subpage_load_script

			# write the file...
			common.gen_page( "%s.html" % page_name, style, content, head_script, load_script )
	
		
