#
# Configuration...
#

TEMPLATE_ASSETS_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFlhZlgwc292b0poYjY3X2JYaU5SRWc&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os

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

def expand_item( asset_def, template_dct ):
        print "asset_def->", asset_def
        asset_name = asset_def["abbrev"]

	style = ""
	content = ""

	atype = asset_def["type"]
	if atype=="img":
		style, content = emit_item( asset_def )

	return [style,content]

def render_template(template_dct):
	tot_style = ""
	tot_content = ""
	for item_key in template_dct.keys():
		item_def = template_dct[ item_key ] [0]
		style, content = expand_item( item_def, template_dct )
		tot_style += style
		tot_content += content
	return [ tot_style, tot_content ]

def get_dct():
	items = common.parse_spreadsheet1( PAGE_TEMPLATE_DEF )
	dct = common.dct_join( items,'page_code')
	print dct

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

