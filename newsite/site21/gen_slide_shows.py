#
# Configuration...
#

SLIDE_SHOW_DEFS = { "whoweare": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEdJVkZzYkRNNF9vdllIVlFYYVFQVFE&output=csv",
	"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDNWT3dveVQxaWdjV1dHY3ZUSnp6VkE&output=csv" }

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

	# prep some global action functions...
	action_scripts = {}
	for pagekey2 in item_def.keys():
		funcname = "func_%s_%s" % ( asset_name, pagekey2 )
		action_scripts[funcname] = None;
	funcname = "func_%s_off " % ( asset_name )
	action_scripts[funcname] = None

	# accumulate the child elements...
	tot_style = ""
	tot_content = ""
	tot_scripts = ""
	all_on = ""
	all_off = ""
	init_script = False

	# NOTE: WE DONT DO SCRIPTS TIL END...

	# insert parent div...
	tot_style += common.emit_line("#%s {" % asset_name)
	tot_style += common.emit_line(" visibility:inherit;")
	tot_style += common.emit_line(" width:100px;")
	tot_style += common.emit_line(" height:100px;")
	tot_style += common.emit_line(" background-color:green;")
	tot_style += common.emit_line("}")
	tot_content += common.emit_line("<div id=%s >" % asset_name )

	dopage=1
	while (True):
		if not item_def.has_key( str(dopage) ):
			break

		# Create a div for each slide in slide show...	
		divname = common.get_id( "%s_%d" % ( asset_name, dopage ), accum_ids )
		accum_ids.append(divname)
		style  = ""
		style += common.emit_line("#%s {" % divname )
		style += common.emit_line(" top:0px;")
		style += common.emit_line(" left:0px;")
		if dopage==1:
			style += common.emit_line(" visibility:inherit;")
		else:
			style += common.emit_line(" visibility:inherit;")
		style += common.emit_line("}")
		tot_style += style
		tot_content  += common.emit_line("<div id=%s >" % divname)
	
		# Accumulate the scriptlet to turn each slide item on/off for this page...
		tot_onscrl = "document.getElementById('%s').style.visibility='visible';" % divname
		tot_offscrl = "document.getElementById('%s').style.visibility='hidden';" % divname
	
		pagedef = item_def[str(dopage)]
		for page_item in pagedef:
			page_asset_name = page_item["asset_name"]
			
			if ( page_asset_name.startswith("img") ):

				# determine script, if any...
				script = None
				if page_item.has_key("link") and page_item["link"]!="":
					link = page_item["link"]
					ltype,parm = link.split(":")
					if ltype=="page":
						funcname = "func_%s_%s" % ( asset_name, parm )
						test = action_scripts[funcname]
						script = "%s ();" % funcname
					else:
						print "ERROR: unknown link type", ltype
						sys.exit(1)

				# determine init vis, if any...
				init_vis = "inherit"
	
				style, content, script, scriptlet_dct = gen_images.expand_item( accum_ids, page_item, images_dct, script, init_vis )
				tot_style += style
				tot_content += content
				tot_scripts += script
				tot_onscrl += scriptlet_dct["on"]
				tot_offscrl += scriptlet_dct["off"]

			elif ( page_asset_name.startswith("mp") ):
				
				style, content = gen_movie_panels.expand_item( accum_ids, page_item, images_dct, movies_dct, movie_panels_dct )
				tot_style += style
				tot_content += content
			
			elif ( page_asset_name.startswith("ss") ):

				style, content = gen_slide_show.expand_item( accum_ids, page_item, images_dct, movies_dct, movie_panels_dct )
				tot_style += style
				tot_content += content

			else:
				print "ERROR: Cannot process->", page_item
				sys.exit(1)

		tot_content  += common.emit_line("</div>")

		# deal with action scripts for this page...
        	funcname = "func_%s_%d" % ( asset_name, dopage )
		action_scripts[funcname] = tot_onscrl;
		
		all_on += tot_onscrl
		all_off+= tot_offscrl

		# the init script is first page...
		if not init_script:
			init_script = "%s ();" % funcname

		dopage += 1

	# end parent div...
	tot_content += common.emit_line("</div>")

	# accumulate the scriptlet dct for this control...
	scriptlet_dct = {}
	scriptlet_dct['on'] = all_off + init_script
	print "SCRIPTDCT ON->", scriptlet_dct['on']
	scriptlet_dct['off'] = all_off

	# finalize the global action script dct for this control...
	# create an all off...
        funcname = "func_%s_off " % ( asset_name )
        action_scripts[funcname] = all_off

	# add to header scripts...	
	for item in action_scripts.keys():
		funcdef = "function %s () { %s; }" % (item, all_off + action_scripts[item] )
		tot_scripts += "\n\n" + funcdef

        return [ tot_style, tot_content, tot_scripts, scriptlet_dct ]

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
		pagedct = common.dct_join( items,'name','page')
		for ky in pagedct.keys():
			newdct[ky] = pagedct[ky]

	#print
	#print
	#print "SS DCT->", newdct
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
