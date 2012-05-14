import xpath
import xml.dom.minidom
import os
import sys
import glob

ASSET_DCT = {}

OPTIONS_DCT = {}
	
def locateAsset(expr):
	png = glob.glob( "./" + expr)
	if len(png)==1: return png[0]
	else: return False

def getAssets():
	global ASSET_DCT
	i = 1
	while (True):
		menu_off = locateAsset("%02d_off*.png" % i )
		if not menu_off: break
		menu_on = locateAsset("%02d_on*.png" % i)
		if not menu_on: break
		main = locateAsset("%02d_main*.png" % i)
		if not main: break
		ASSET_DCT[i] = { 'menu_off': menu_off, 'menu_on':menu_on, 'main':main }
		i += 1
	print "INFO: assets->",ASSET_DCT


def processOptionNode(i, node):

	print "ProcessOptionNode->", node, node.nodeName
	nodes = xpath.find("/menu", node)
	print len(nodes)

	global OPTIONS_DCT
	menu_x = int( xpath.find( "menu",node )[0].attributes["x"].value )
	menu_y = int( xpath.find( "menu",node )[0].attributes["y"].value )
	main_x = int( xpath.find( "main",node )[0].attributes["x"].value )
	main_y = int( xpath.find( "main",node )[0].attributes["y"].value )

	option = ASSET_DCT[i]
	option["menu_x"] = menu_x
	option["menu_y"] = menu_y
	option["main_x"] = main_x
	option["main_y"] = main_y

	OPTIONS_DCT[i] = option

	print "INFO: option->", i, option

def emitLine(f,str):
	f.write("%s\n" % str)

def emitMenu(f, i, option, on):
	print "EMITMENU: ", i, option, on

	if on:
		htmlid = "optionmenu_on_%02d" % i
	else:
		htmlid = "optionmenu_off_%02d" % i

	emitLine(f,"<style>")
	emitLine(f," #%s {" % htmlid )
	emitLine(f," position: absolute;")
	emitLine(f," left: %02dpx;" % option["menu_x"]);
	emitLine(f," top: %02dpx;" % option["menu_y"])
	emitLine(f," z-index: 0;" )
	emitLine(f," overflow: hidden;" )
	emitLine(f," border: 0px;" )
	emitLine(f,"}")
	emitLine(f,"</style>")

	if on:
		emitLine(f,"<img id=\"%s\" src=\"%s\" />" %  (htmlid, option["menu_on"]))
	else:
		emitLine(f,"<a href=\"%s\"><img id=\"%s\" src=\"%s\" /></a>" % \
			("%02d.html" % i, htmlid, option["menu_off"]))

def emitMain(f, i, option ):
        htmlid = "optionmain%02d" % i

        emitLine(f,"<style>")
        emitLine(f," #%s {" % htmlid )
        emitLine(f," position: absolute;")
        emitLine(f," left: %02dpx;" % option["main_x"]);
        emitLine(f," top: %02dpx;" % option["main_y"])
        emitLine(f," z-index: 0;" )
        emitLine(f," overflow: hidden;" )
        emitLine(f," border: 0px;" )
        emitLine(f,"}")
        emitLine(f,"</style>")

        emitLine(f,"<img id=\"%s\" src=\"%s\" />" %  (htmlid, option["main"]))


def emitHTML():
	global OPTIONS_DCT

	i = 1
	while (True):
		if not OPTIONS_DCT.has_key(i): break
		option = OPTIONS_DCT[i]

		f  = open("%02d.html" % i,"w")
		emitLine(f,"<html>")
		emitLine(f,"<body>")

		for m in OPTIONS_DCT.keys():
			emitMenu(f, m, OPTIONS_DCT[m], m==i)
		
		emitMain(f,i,option)

		emitLine(f,"</body>")
		emitLine(f,"</html>")

		f.flush()
		f.close()

		i += 1

def processSimpleMenu(scheme):

	# get the assets per simple menu schema...
	getAssets()

	#iterate consec...
	i = 1
	while (True):
		xp = "//option[@item = %02d]" % i
		nodes = xpath.find(xp, scheme)
		if len(nodes)==0: break
		node = nodes[0]
		processOptionNode(i,node)
		i += 1
	
	# process the dct...
	emitHTML()
	
def parseDocument():

	# get top level document...
	d = xml.dom.minidom.parse("scheme.xml")

	# get scheme node...
	scheme = d.childNodes[0]

	# get type...
	type = scheme.attributes["type"].value

	if type == "simplemenu":
		return processSimpleMenu(scheme)
	else:
		print "ERROR: Unknown scheme type"
		sys.exit(1)

if __name__ == "__main__":

	parseDocument()
