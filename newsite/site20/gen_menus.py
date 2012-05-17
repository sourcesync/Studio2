#
# Configuration...
#

MENUS_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDZCVTJodXFXOXFjMjNFb0o5WnpFTkE&output=csv"

#
# Library...
#
import common
import gen_images

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
	print "SCRIPTS->", script
	return script	

def expand_option( menu_def, option_name, images_dct, option_script_dct ):
	option_def = menu_def[option_name]
	tot_style = ""
	tot_content = ""
	for item in option_def:
		print "option item->", item
		asset_name = item["asset_name"]
		if asset_name.startswith("img"):

			# determine the script, if any...
			script = None
			if item.has_key("link") and item("link")!="":
        			link = asset_def["link"]
                		ltype,parm = link.split(":")
                		if ltype=="option":
                        		script = option_script_dct[parm]
				else:
					print "ERROR: Unknown link type"
					sys.exit(1)	

			style, content = gen_images.expand_item( item, images_dct, script )
			tot_style += style
			tot_content += content

	return [ tot_style, tot_content ]

def expand_item(item, images_dct, menus_dct):
	print "expand->",item
	key = item["asset_name"]
	menu_def = menus_dct[key]
	print "menu_def->", menu_def
	scripts = create_option_scripts( key, menus_dct)
	print "SCRIPTS->",scripts
	tot_style = ""
	tot_content = ""
	for key in menu_def.keys():
		style, content = expand_option( menu_def, key, images_dct, scripts )
		tot_style += style
		tot_content += content
	return [ tot_style, tot_content ]

def get_dct():
	items = common.parse_spreadsheet1( MENUS_DEF )
	dct = common.dct_join( items,'menu_name','option_name')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct
