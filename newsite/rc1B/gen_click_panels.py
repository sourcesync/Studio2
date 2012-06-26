#
# Configuration...
#

CLICK_PANEL_DEFS = { "photos":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedEFLTGNNcHNhNmRCWHljUzlzN01SZ2c&output=csv", \
	"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGh4NEQ4Q195dlM0Y3hIX2M5enZvcUE&output=csv" }

#
# Library...
#
import common
import os
import gen_images
import sys

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../videos"
VIDEOS_PREFIX = "../videos"
POSTERS_PREFIX = "../posters"


def get_dct(pagekeys):
	print "cp getdct->", pagekeys
        if pagekeys==None:
                pagekeys = CLICK_PANEL_DEFS.keys()
        newdct = {}
        for code in pagekeys:
                if not CLICK_PANEL_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( CLICK_PANEL_DEFS[code], "click panels->%s" % str(pagekeys) )
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

def cpo_expand_preview_item( accum_ids, parent, asset_def, cp_dct, cpo_dct, images_dct, init_item, action_scripts ):

        print "CPO EXPAND PREVIEW->", asset_def, cpo_dct.keys()

        typ = asset_def["type"]
        x = int(asset_def['x'])
        y = int(asset_def['y'])
        z = int(asset_def['z'])
        name = asset_def['asset_name']
        hid = common.get_id( name, accum_ids )

        # get the individual images and create ids...
        img_init_asset = images_dct[init_item][0]
        path = img_init_asset['path']
        fname = img_init_asset['filename']
        src = os.path.join(path,fname)
        src = common.path_replace( src )
       	src = common.create_path( src )
 
	# style...
        style = ""
        style += common.emit_line("#%s {" % hid )
        style += common.emit_line(" position: absolute;")
        style += common.emit_line(" top: %dpx;" % y )
        style += common.emit_line(" left: %dpx;" % x )
        style += common.emit_line(" z-index: %d;" % (z+1) )
        style += common.emit_line(" border:none;" )
        style += common.emit_line(" visibility: hidden;" )
        style += common.emit_line("}")

	# content...
        content = "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\"  />\n"  % (hid, src)

	# scriptlet dct...
	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % hid
	scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % hid
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % hid

	return [ style, content, scriptlet_dct ]

def cpo_expand_caption_item( accum_ids, parent, asset_def, cp_dct, cpo_dct, images_dct, init_item, action_scripts ):

        print "CPO EXPAND CAPTION->", asset_def, cpo_dct.keys()

        typ = asset_def["type"]
        x = int(asset_def['x'])
        y = int(asset_def['y'])
        z = int(asset_def['z'])
        name = asset_def['asset_name']
        hid = common.get_id( name, accum_ids )

        # get the individual images and create ids...
        img_init_asset = images_dct[init_item][0]
        path = img_init_asset['path']
        fname = img_init_asset['filename']
        src = os.path.join(path,fname)
        src = common.path_replace( src )
        src = common.create_path( src )
	print "init src->", src

        # style...
        style = ""
        style += common.emit_line("#%s {" % hid )
        style += common.emit_line(" position: absolute;")
        style += common.emit_line(" top: %dpx;" % y )
        style += common.emit_line(" left: %dpx;" % x )
        style += common.emit_line(" z-index: %d;" % (z+1) )
        style += common.emit_line(" border:none;" )
        style += common.emit_line(" visibility: hidden;" )
        style += common.emit_line("}")

        # content...
        content = "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\"  />\n"  % (hid, src)

        # scriptlet dct...
        scriptlet_dct = {}
        scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % hid
        scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % hid
        scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % hid

        return [ style, content, scriptlet_dct ]


def cpo_expand_option_item( accum_ids, parent, asset_def, cpo_dct, images_dct, init_option, action_scripts ):
	
	print "CPO EXPAND->", asset_def, cpo_dct.keys()

	typ = asset_def["type"]
	x = int(asset_def['x'])
	y = int(asset_def['y'])
	z = int(asset_def['z'])
	name = asset_def['asset_name']
	hid = common.get_id( name, accum_ids )

	# get the option asset...
	cpo_asset = cpo_dct[ name ][0]

	# get the individual images and create ids...
	img_desel = cpo_asset['deselected']
	desel_id = "%s_desel" % hid
	img_sel = cpo_asset['selected']
	sel_id = "%s_sel" % hid
	img_preview = cpo_asset['preview']		

	# desel style...
	style = ""	
	style += common.emit_line("#%s {" % desel_id )
	style += common.emit_line(" position: absolute;")
	style += common.emit_line(" top: %dpx;" % y )
	style += common.emit_line(" left: %dpx;" % x )
	style += common.emit_line(" z-index: %d;" % (z+1) )
	style += common.emit_line(" border:none;" )
	style += common.emit_line(" visibility: hidden;" )
	style += common.emit_line("}")

	# sel style...
        style += common.emit_line("#%s {" % sel_id )
        style += common.emit_line(" position: absolute;")
        style += common.emit_line(" top: %dpx;" % y )
        style += common.emit_line(" left: %dpx;" % x )
        style += common.emit_line(" z-index: %d;" % z )
        style += common.emit_line(" border:none;" )
        style += common.emit_line(" visibility: hidden;" )
        style += common.emit_line("}")

	# create scriptlet dcts...
	master_scr_dct = []

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % desel_id
	scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % desel_id
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % desel_id
	master_scr_dct.append( scriptlet_dct )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % sel_id
	scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % sel_id
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % sel_id
	master_scr_dct.append( scriptlet_dct )

	# create the content...
	content = ""

	# desel...
	img_desel_asset = images_dct[img_desel][0]
	path = img_desel_asset['path']	
	fname = img_desel_asset['filename']	
	src = os.path.join(path,fname)
        src = common.path_replace( src )
	content += "<a href=\"#\" >\n"
	#content += "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\" onclick=\"%s;\" onmouseover=\"%s;\" onmouseout=\"%s;\" />\n" % \
	#(desel_id, src, "%s_click()" % desel_id, "%s_mouseover()" % desel_id, "%s_mouseout()" % desel_id )
	content += "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\" onclick=\"%s;\"  />\n" % \
		(desel_id, src, "%s_click()" % desel_id )
	content += "</a>\n"

	# sel...
	img_sel_asset = images_dct[img_sel][0]
	path = img_sel_asset['path']	
	fname = img_sel_asset['filename']	
	src = os.path.join(path,fname)
        src = common.path_replace( src )
	content += "<a href=\"#\" >\n"
	#content += "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\" onclick=\"%s;\" onmouseover=\"%s;\" onmouseout=\"%s;\" />\n" % \
	#(sel_id, src, "%s_click()" % sel_id, "%s_mouseover()" % sel_id, "%s_mouseout()" % sel_id )
	content += "<img id=\"%s\" src=\"%s\" alt=\"TheStudio\" onclick=\"%s;\"  />\n" % \
		(sel_id, src, "%s_click()" % sel_id )
	content += "</a>\n"

	return [ style, content, master_scr_dct ]

	

def expand_item( accum_ids, asset_def, images_dct, movies_dct, movie_panels_dct, click_panels_dct, cpo_dct ):
	
	print "CLICK PANELS EXPAND->", asset_def, asset_def["asset_name"], "cp->",click_panels_dct.keys(), "cpo->", cpo_dct.keys()

	asset_name = asset_def["asset_name"]
	item_def = click_panels_dct[asset_name]
	print "ITEM DEF->", item_def

	tot_style = ""
	tot_content = ""
	tot_on = ""
	tot_off = ""
	init_script = ""

	# get the init option...
	init_option = asset_def['init']
	print "init_option->", init_option

	# find the main preview item...
	preview_def = None
        for item in item_def:
                asn = item["asset_name"]
                typ = item["type"]
                if asn.startswith("cpo") and (typ=="preview"):
			preview_def = item
			break
	if not preview_def:
		print "ERROR: gen_click_panels: Could not find preview item"
		sys.exit(1)
	preview_id = preview_def['asset_name']

        # find the main caption item...
        caption_def = None
        for item in item_def:
                asn = item["asset_name"]
                typ = item["type"]
                if asn.startswith("cpo") and (typ=="caption"):
                        caption_def = item
                        break
        if not caption_def:
                print "ERROR: gen_click_panels: Could not find caption item"
                sys.exit(1)
        caption_id = caption_def['asset_name']

	# prepare action script dct...
        action_scripts = {}
	action_scripts['common_show'] = "function show(id) { if (id!=null) document.getElementById(id).style.visibility='visible';}"
	action_scripts['common_hide'] = "function hide(id) { if (id!=null) document.getElementById(id).style.visibility='hidden';}"
	action_scripts['common_preview'] = "function preview(id,path,capid,cappath) { document.getElementById(id).src = path; document.getElementById(capid).src=cappath;}"
	action_scripts['global'] = "var %s_sel = null; var %s_desel = null;" % (asset_name, asset_name )
	for item in item_def:
		asn = item["asset_name"]
		if asn.startswith("cpo"):

			typ = item["type"]
			if typ != "option": continue

			asn_def= cpo_dct[asn][0]
			img_desel = asn_def['deselected']
			img_sel = asn_def['selected']
			img_preview = asn_def['preview']
			img_caption = asn_def['caption']

			# get path to img preview...
			print "IMAGES->", asn, item, images_dct.keys()
			img_preview_asset = images_dct[img_preview][0]
			path = img_preview_asset['path']
			fname = img_preview_asset['filename']
			src = os.path.join(path,fname)
			src = common.path_replace( src )

			# get path to caption...
			img_caption_asset = images_dct[img_caption][0]
			print "img->",img_caption_asset
			path = img_caption_asset['path']
			fname = img_caption_asset['filename']
			capsrc = os.path.join(path,fname)
			capsrc = common.path_replace( capsrc )

			desel_id = "%s_desel" % asn
			sel_id = "%s_sel" % asn

			# do desel scripts...
			action_scripts["%s_desel_click" % asn] = "function %s_desel_click() "  % asn + \
				"{ show( %s_desel ); hide( %s_sel ); show( '%s' ); hide( '%s' ); " % \
					( asset_name, asset_name, sel_id, desel_id ) + \
				" %s_sel = '%s'; %s_desel = '%s'; " % ( asset_name, sel_id, asset_name, desel_id ) + \
				"preview( '%s','%s','%s','%s');} " % (preview_id, src, caption_id, capsrc)
	
			# do sel scripts...
			action_scripts["%s_sel_click" % asn] = "function %s_sel_click() {} "  % asn 

	for item in item_def:
		asn = item["asset_name"]
		typ = item["type"]

		if asn.startswith("cpo") and (typ=="option"):
			# expand the cpo item...
			style, content, master_dct = cpo_expand_option_item( accum_ids, asset_name, item, cpo_dct, images_dct, init_option, action_scripts )
			tot_style += style
			tot_content += content

			# desel...
			tot_on += master_dct[0]['on']
			tot_off += master_dct[0]['off']
			init_script += master_dct[0]['init']
		
			# sel...	
			tot_on += master_dct[1]['on']
			tot_off += master_dct[1]['off']
			init_script += master_dct[1]['init']

                elif asn.startswith("cpo") and (typ=="preview"):

			init_img = item['init']

                        # expand the cpo item...
                        style, content, scriptlet_dct = \
				cpo_expand_preview_item( accum_ids, asset_name, item, click_panels_dct, cpo_dct, images_dct, init_img, action_scripts )
                        tot_style += style
                        tot_content += content

                        # desel...
                        tot_on += scriptlet_dct['on']
                        tot_off += scriptlet_dct['off']
                        init_script += scriptlet_dct['init']

		elif asn.startswith("cpo") and (typ=="caption"):

                        init_img = item['init']

                        # expand the cpo item...
                        style, content, scriptlet_dct = \
                                cpo_expand_caption_item( accum_ids, asset_name, item, click_panels_dct, cpo_dct, images_dct, init_img, action_scripts )
                        tot_style += style
                        tot_content += content

                        # desel...
                        tot_on += scriptlet_dct['on']
                        tot_off += scriptlet_dct['off']
                        init_script += scriptlet_dct['init']

		else:
			print "ERROR: Click_Panel: Cannot process asset->", item
			sys.exit(0)

	scriptlet_dct = {}
	scriptlet_dct['on'] = tot_on
	scriptlet_dct['off'] = tot_off
	scriptlet_dct['init'] = init_script
	
	if init_option:
		scriptlet_dct['init'] += "show('%s');hide('%s');" % ( '%s_sel' % init_option, '%s_desel' % init_option ) + \
			"cp_photos_sel = '%s'; cp_photos_desel = '%s';" % ( '%s_sel' % init_option, '%s_desel' % init_option )
		print scriptlet_dct['init']

	load_script = ""
	for key in action_scripts.keys():
		load_script += action_scripts[key] + "\n"	

	return [ tot_style, tot_content, load_script, scriptlet_dct ]


if __name__ == "__main__":
	dct = get_dct()
	print dct
