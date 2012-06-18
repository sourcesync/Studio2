#
#
# Configuration...
#

#IMAGES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFd0ZV81SS1yZmZqQnpGdVBUeTlvVEE&output=csv"

IMAGES_DEFS = { "map":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHI5LTQzdi1kOFJHaE1Kb050ajY5RkE&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

EMBEDS_DIR = "embeds"

#
# Library...
#
import common
import os


def get_attr( prop, asset_name, asset_def, embeds_dct, default=None):
	if asset_def.has_key(prop):
		return asset_def[prop]
	else:
		item_def = embeds_dct[asset_name][0]
		if item_def.has_key(prop) and item_def[prop]!='':
        		val = item_def[prop]
			return val	
		elif default!=None:
			print "WARNING: Returning default value->", default, prop, asset_name
			return default
		else:
			return False

def expand_item( accum_ids, asset_def, embeds_dct ):

	# get the asset definition...
        asset_name = asset_def["asset_name"]
	print "ed->", embeds_dct
        item_def = embeds_dct[asset_name][0]

	# get id...
        htmlid = common.get_id(asset_name,accum_ids)
	accum_ids.append( htmlid )

	# get basic properties...
	codeval = item_def['code']
	if codeval.startswith("file"):
		idx = codeval.find(":") + 1
		filename = codeval[idx:]
		path = os.path.join(EMBEDS_DIR, filename)
		f = open(path,'r')
		code = f.read()
		f.close()	

		# insert id...
		print "CODEVAL-->%s<--" % code, code.startswith("<div ")
		if ( code.startswith("<div ") ):
			code = code[0:5] + " id=%s " % htmlid + code[5:]
			print "REPLACE 1!!", code

	else:
		print "ERROR: Invalid code value"
		sys.exit(1)	

        x = get_attr( 'x', asset_name, asset_def, embeds_dct )
        y = get_attr( 'y', asset_name, asset_def, embeds_dct )
        z = get_attr( 'z', asset_name, asset_def, embeds_dct,'0')
	
	# style...
	style  = ""
        style += common.emit_line( "#%s {" % htmlid )
        style += common.emit_line( "position: absolute;")
        style += common.emit_line( "left: %dpx;" % int(x) )
        style += common.emit_line( "top: %dpx;" % int(y) )
        style += common.emit_line( "z-index: %d;" % int(z) )

	# content...

	content = common.emit_line( code )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )
	scriptlet_dct['off']  = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'hidden' )
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility = '%s';" % (htmlid, 'visible' )

        return [ style, content, "", scriptlet_dct ]

def get_item_path( name, images_dct ):
        item_def = images_dct[name][0]
        path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("PHIL",PHIL_PREFIX)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        return fpath

def get_dct( pagekeys=None ):
	if pagekeys==None:
		pagekeys = IMAGES_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not IMAGES_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( IMAGES_DEFS[code] )
		print "it->", code, pagekeys, IMAGES_DEFS[code], type(items), items
		dct = common.dct_join( items,'name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
