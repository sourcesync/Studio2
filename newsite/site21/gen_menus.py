#
# Configuration...
#

#MENUS_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDZCVTJodXFXOXFjMjNFb0o5WnpFTkE&output=csv"

MENUS_DEFS = { "clients":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFdDRm1sTDVndGpfcVplamRtRWllU2c&output=csv",\
	"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEkzVm1qWE13MklHZ0Q5bk5VOEdzZlE&output=csv", \
	"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHNZR1hwZWswcXQ3NEIxSjQ0S0hpY3c&output=csv", \
	"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDdjLWp3cGFZbHk0bUdKNTZCMDlBcHc&output=csv", \
	"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGlMZjVOSm40SzM1d1JBcW9IVjRIY3c&output=csv", \
	"motiondesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFhaNkRlLWp1OVZldDc3R0h4VldHdGc&output=csv", \
	"animation":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGMxeWcybnpzemtEVFdRbXlIS3ZtMWc&output=csv" }

#
# Library...
#
import common
import gen_images
import gen_slide_shows

def create_option_script( asset_name, option, menus_dct ):
	menu_def = menus_dct[asset_name]
	script = ""
	for key in menu_def.keys():
		option_def = menu_def[key]
		for item in option_def:
			itemid = item["asset_name"]
			#script += "alert('%s');" % itemid
			if key == option:
				script += "document.getElementById('%s').style.visibility='visible';" % itemid
			else:
				script += "document.getElementById('%s').style.visibility='hidden';" % itemid
	return script

def create_option_scripts( asset_name, menus_dct ):
	script = {}
	menu_def = menus_dct[asset_name]
	for key in menu_def.keys():
		script[key] = create_option_script( asset_name, key, menus_dct )
	return script	

def expand_option( accum_ids, menu_name, menu_def, option_name, images_dct, action_scripts, init_hidden, slide_shows_dct ):
	option_def = menu_def[option_name]

	tot_style = ""
	tot_content = ""
	tot_scripts = ""
	off_scriptlet = ""
	on_scriptlet= ""
	init_scriptlet = ""

	for item in option_def:
		asset_name = item["asset_name"]

		if asset_name.startswith("img"):

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
					print "ERROR: Unknown link type"
					sys.exit(1)	

			# determine initial css visibility, if any...
			init_vis = None
			if item.has_key("init") and item["init"]!="":
				init_vis = item["init"] 
			style, content, script, scriptlet_dct = gen_images.expand_item( accum_ids, item, images_dct, script, init_vis, ahref )

			tot_style += style
			tot_content += content
			tot_scripts += script

			# accumulate on/off scriptlet...
			off_scriptlet += scriptlet_dct['off']	
			on_scriptlet += scriptlet_dct['on']	

		elif asset_name.startswith("ss"):

			style, content, script, scriptlet_dct = gen_slide_shows.expand_item( accum_ids, item, images_dct, None, None, None, slide_shows_dct )

			tot_style += style
			tot_content += content
			tot_scripts += script

			# accumulate on/off scriptlet...
                        off_scriptlet += scriptlet_dct['off']
                        on_scriptlet += scriptlet_dct['on']

		else:
			print "ERROR: Can't process asset->", asset_name, item
			sys.exit(1)

	scriptlet_dct = {}
	scriptlet_dct['on'] = on_scriptlet
	scriptlet_dct['off'] = off_scriptlet
	scriptlet_dct['init'] = init_scriptlet

	return [ tot_style, tot_content, tot_scripts, scriptlet_dct ]

def expand_item(accum_ids, item, images_dct, menus_dct, slide_shows_dct ):
	menu_name = item["asset_name"]
	menu_def = menus_dct[menu_name]

	# pre the global scripts from scriptlets...
	action_scripts = {}
	for option in menu_def.keys():
		funcname = "func_%s_%s" % ( menu_name, option )
		action_scripts[ funcname ] = None

	# iterate individual assets and expand...
	tot_style = ""
	tot_content = ""
	tot_script = ""
	scriptlets_dct = {}
	init_script = False

	# iterate the options...
	for option in menu_def.keys():
		style, content, script, scriptlet_dct = expand_option( accum_ids, menu_name, menu_def, option, images_dct, action_scripts, True, slide_shows_dct )
		tot_style += style
		tot_content += content
		tot_script += script
		scriptlets_dct[option] = scriptlet_dct
		# first option is the init...
		if not init_script:
			init_script = scriptlets_dct[option]['on']

        # create a total off scriplet for menu...
        tot_off = ""
        for option in scriptlets_dct.keys():
                tot_off += scriptlets_dct[option]['off']

	# finalize the action script dct...
	for option in menu_def.keys():
		funcname = "func_%s_%s" % ( menu_name, option )
		funcdef = "function %s () { %s };" % ( funcname, tot_off + scriptlets_dct[option]['on'] )
		action_scripts[ funcname ] = funcdef
	
	# append to header script...
	for item in action_scripts.keys():
		tot_script += "\n\n" + action_scripts[item]

	# scriptlet dct...
	scriptlet_dct = {}
	scriptlet_dct['off'] = tot_off
	scriptlet_dct['on'] = tot_off + init_script

	return [ tot_style, tot_content, tot_script, scriptlet_dct ]

def get_dct( pagekeys=None ):
	
	if pagekeys==None:
		pagekeys = MENUS_DEFS.keys()

	newdct = {}
	for code in pagekeys:	
		if ( not code in pagekeys): continue
		items = common.parse_spreadsheet1( MENUS_DEFS[code] )
		dct = common.dct_join( items,'menu_name','option_name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]	
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
