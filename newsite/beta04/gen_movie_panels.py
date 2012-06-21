#
# Configuration...
#

MOVIE_PANEL_DEFS = { \
	"animation_gallery":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEg4VGhhZzVKNU5JdmE4ejhfLUNtVmc&output=csv", \
	"motiondesign_gallery":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedG1GWkRVUWtQdl9sOFZWcDhpd1ZrYnc&output=csv", \
	"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDNvUDE2NVVCRTgxQ2M3OFpRbnIyaWc&output=csv", \
	"interactive":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedHg2cGstNGI4bk1WZHpma0p6RG5STVE&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os
import sys
import gen_movies
import gen_images

def get_dct( pagekeys=None ):
        if pagekeys==None:
                pagekeys = MOVIE_PANEL_DEFS.keys()
        newdct = {}
        for code in pagekeys:
                if not MOVIE_PANEL_DEFS.has_key(code): continue
                items = common.parse_spreadsheet1( MOVIE_PANEL_DEFS[code], "movie panels %s" % str(pagekeys) )
                dct = common.dct_join( items,'name')
                for ky in dct.keys():
                        newdct[ky] = dct[ky]
        return newdct

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
	scriptlet_dct = {}
	scriptlet_dct['on'] = ''
	scriptlet_dct['off'] = ''
	scriptlet_dct['init'] = ''

	htmlid = common.get_id( asset_name, accum_ids )
	accum_ids.append( htmlid )

	for item in item_def:

		asn = item["asset_name"]
		if asn.startswith("mov"):
			style, content, scr_dct = gen_movies.expand_item( accum_ids, item, images_dct, movies_dct )
			tot_style += style
			tot_content += content

			scriptlet_dct['on'] += scr_dct['on']
			scriptlet_dct['off'] += scr_dct['off']
			scriptlet_dct['init'] += scr_dct['init']
		
		elif asn.startswith("img"):
			# determine the script, if any...
                        script = None
                        ahref = None
                        if item.has_key("link") and item["link"]!="":
                                link = item["link"]
                                if link.startswith("option:"):
                                        ltype,parm = link.split(":")
                                        funcname = "func_%s_%s" % (menu_name, parm)
                                        test = action_scripts[funcname]
                                        script = "%s ();" % funcname
                                elif link.startswith("url:"):
                                        idx = link.find(":") + 1
                                        ahref = link[idx:]
                                        print "MENUS AHREF->", ahref
                                else:
                                        print "ERROR: Unknown link type", asset_name, item
                                        sys.exit(1)    

			style, content, foo, scr_dct = gen_images.expand_item( accum_ids, item, images_dct, script, None, ahref )
			tot_style += style
			tot_content += content
	
			scriptlet_dct['on'] += scr_dct['on']
			scriptlet_dct['off'] += scr_dct['off']
			scriptlet_dct['init'] += scr_dct['init']

		else:
			print "ERROR: Cannot process->", item
			sys.exit(1)			


	
	return [ tot_style, tot_content, scriptlet_dct ]

if __name__ == "__main__":
	dct = get_dct()
	print dct
