#
# Configuration...
#

PAGE_TEMPLATE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFlhZlgwc292b0poYjY3X2JYaU5SRWc&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os
import copy
import sys

def anim_script_item( anim, srcid, template_dct, template_assets_dct ):
        a = anim[0]
        b = anim[1]
	page_dct = template_dct
	other_dct = template_assets_dct
	prefix = ""

        if (b=="show"):
                nm = a
                if page_dct.has_key(nm):
                        info = page_dct[nm][0]
                else:
                        info = otherdct[nm][0]

                fpath = os.path.join( info["file_location"], info["file_name"] )   #info['fp']
                if prefix: fpath = os.path.join(prefix,fpath)
                script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (nm,nm,fpath)
        elif ( b=="hide"):
                nm = a
                script = "document.getElementById('%s').style.visibility='hidden';" % nm
        elif ( b=="replace" ):
                nm = a
                info = page_dct[nm][0]
                fpath = os.path.join( info["file_location"], info["file_name"] )   #info['fp']
                if prefix: fpath = os.path.join(prefix,fpath)
                script = "document.getElementById('%s').style.visibility='visible';document.getElementById('%s').src='%s'" % (srcid,srcid,fpath)
        return script


def emit_item(item, template_dct, template_assets_dct ):

	nm = item["abbrev"]
	x = int( item["x"] )
	y = int( item["y"] )
	z = 0
	eltype = item["type"]
	file_location = item["file_location"]
	file_name = item["file_name"]
	fpath = os.path.join(file_location,file_name)

	# emit style...
	html = ""
	style = ""
	style += "#%s {\n" % nm
	style += "position: absolute;"
	style += "left: %dpx;\n" % x
	style += "top: %dpx;\n" % y
	style += "z-index: %d;\n" % z
	style += "overflow: hidden;\n"
	style += "border: 0px;\n"
	#html += "border: 1px dashed #333;"
	if eltype == 'imganim':
		style += "visibility: hidden;\n"
	style += "}\n"
	style += "#%s.hover { border: 1px dashed #333; }\n" % nm

	# get link...
	link = item["link"]

	# get mouseover script, if any...
	mover = ""
	if item["mouseover"] != "":
		anim = item["mouseover"].split(":")
		mover = anim_script_item( anim, nm, template_dct, template_assets_dct )

	# get mouseout script, if any...
        mout = ""
	if item["mouseover"] != "":
		anim = item["mouseout"].split(":")
		mout = anim_script_item( anim, nm, template_dct, template_assets_dct )

	mc = ""
	
	# emit the item...
	if eltype=="imgmovie":
		pass
        elif mc!="":
		pass
        elif link:
                html += '<a href="%s">' % (link+'.html')
                html += '<img id=%s src="%s" onmouseover="%s" onmouseout="%s"  />\n' % (nm,fpath,mover,mout)
                html += '</a>'
        else:
                html += '<img id=%s src="%s" />\n' % (nm,fpath)

        return [ style, html ]

def expand_item( asset_def , template_dct, template_assets_dct ):
        asset_name = asset_def["abbrev"]

	style = ""
	content = ""

	atype = asset_def["type"]
	if atype=="img":
		style, content = emit_item( asset_def, template_dct, template_assets_dct )
	elif atype=="imganim":
		style, content = emit_item( asset_def, template_dct, template_assets_dct )

	return [style,content]

def render_page(page, page_templates_dct, template_dct, template_assets_dct ):
	tot_style = ""
	tot_content = ""

	# copy template dct
	template_dct_cp = copy.deepcopy( template_dct )

	# prepare the render dct...
	render_dct = {}

	# copy over unselected assets...
	for item_key in template_dct_cp.keys():
		render_item = template_dct_cp[item_key][0]
		if render_item["selected"] == "0":
			render_dct[ item_key ] = [ copy.deepcopy(render_item) ]

	# perform operations as defined in page_template dct...
	page_template_items = page_templates_dct[page]
	for page_template_item in page_template_items:

		image_code = page_template_item["image_code"]
		replace = page_template_item["replace"]
		wth = page_template_item["with"]
		replace_x = page_template_item["replace_x"]
		replace_y = page_template_item["replace_y"]
		wth_x = page_template_item["with_x"]
		wth_y = page_template_item["with_y"]
	
		if image_code == "temp" and  replace!="" and render_dct.has_key(replace):

			# first look in template dct...
			if template_dct_cp.has_key(wth):
				findel = template_dct_cp[wth][0]
				render_dct[replace] = [ copy.deepcopy(findel) ]
			# then look in temmplate assets...
			else:
				print "ERROR: For replace, could not find->", wth
				sys.exit(0)
	
		elif image_code != "":

			# first look in template dct...
			if template_dct_cp.has_key(image_code):
				findel = template_dct_cp[image_code][0]
				render_dct[replace] = [ copy.deepcopy(findel) ]
			# then look in temmplate assets...
			elif template_assets_dct.has_key(image_code):
				findel = template_assets_dct[image_code][0]
				render_dct[replace] = [ copy.deepcopy(findel) ]
			else:
				print "ERROR: For replacexy, could not find->", image_code
				sys.exit(0)

			# do any x replace here...
			if replace_x != "" and wth_x !="":
				item = render_dct[replace][0]
				item['x'] = wth_x
			
			# do any y replace here...
			if replace_y != "" and wth_y !="":
				item = render_dct[replace][0]
				item['y'] = wth_y

	
	# do the render...
	for render_item_key in render_dct.keys():
		render_item = render_dct[render_item_key][0]	
		style, content = expand_item( render_item , template_dct, template_assets_dct )
		tot_style += style
		tot_content += content

	return [ tot_style, tot_content ]

def get_dct():
	items = common.parse_spreadsheet1( PAGE_TEMPLATE_DEF )
	dct = common.dct_join( items,'page_code')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct
	style, content = render_template( dct )
	print "STYLE=", style
	print "CONTENT=", content
	f = open("template.html",'w')
	f.write("<html><body>\n")
	f.write("<style>%s</style>\n" % style)
	f.write("%s\n" % content)
	f.write("</body></html>")
	f.flush()
	f.close()
	print "INFO: wrote file-> template.html"

