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

def emit_item(item):

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
	#html += "<style>\n"
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
	#html += "</style>\n"

        mover = ""
        mout = ""
	mc = ""
	link = False
	
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

def expand_item( asset_def ):
        asset_name = asset_def["abbrev"]

	style = ""
	content = ""

	atype = asset_def["type"]
	if atype=="img":
		style, content = emit_item( asset_def )

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
		if image_code == "temp" and  replace!="" and render_dct.has_key(replace):
			# first look in template dct...
			if template_dct_cp.has_key(wth):
				findel = template_dct_cp[wth][0]
				render_dct[replace] = [ copy.deepcopy(findel) ]
			else:
				print "ERROR: Could not find->", wth
				sys.exit(0)
	
	# do the render...
	for render_item_key in render_dct.keys():
		render_item = render_dct[render_item_key][0]	
		style, content = expand_item( render_item )
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

