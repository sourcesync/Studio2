#
# Configuration...
#

TEMPLATE_ASSETS_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFpLb1JBSTMwZzJHM25pVTF0TF9Xc3c&output=csv"

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
                html += '<img id=\"%s\" src="%s" onmouseover="%s" onmouseout="%s"  />\n' % (nm,fpath,mover,mout)
                html += '</a>'
        else:
                html += '<img id=\"%s\" src="%s" />\n' % (nm,fpath)

        return [ style, html ]

def expand_item( asset_def, template_dct ):
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
	items = common.parse_spreadsheet1( TEMPLATE_ASSETS_DEF, "page_template_assets" )
	dct = common.dct_join( items,'abbrev')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct

