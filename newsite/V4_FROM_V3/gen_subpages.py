#
# Configuration...
#

#SUB_PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEllOHZqalNfSlFCaF9oYXF6a3pqTGc&output=csv"

SUB_PAGE_DEFS = { "home":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFpwVkZzOW5zTTF1QTZzNkFuUjFodkE&output=csv", \
	"whoweare":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEptTWZNbG5ZVTI0ZWU4bDluaVNpWHc&output=csv", \
	#"sneakpeek":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE5xR2tvbUl0VEFsZFgzRVVhazR2Q1E&output=csv", \
	"sneakpeek":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDJqR051Mll0cm1GYXdESHZnRnhwRmc&output=csv", \
	"clients":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGRZMTN0b1ZBZ3BiN0ktbDg0X3EyUGc&output=csv", \
	#"contacts":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHU2dGVKWXdLckQxQTZXWFpJZ3kyZ3c&output=csv", \
	"contacts":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEg4SVBZQ1ZmeGRpM2JIXzlTUHNvY1E&output=csv", \
	"community":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGJRcnZvck00R0dIRXZuYkJDVm5iM3c&output=csv",\
	"map":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDhzajRpU1JsdlZ2amFyMGlMekw4a2c&output=csv", \
	"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGpJM1FEVGg3RVhaTHJjcFRwVEtsQXc&output=csv", \
	"photos":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpGaC1Xam5xeFR1MGpwc05aYU1YZlE&output=csv", \
	#"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFhUTFlOQjVqR0VwRVg4UW9YeGc1d1E&output=csv", \
	"mocap":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFVYX3F0MDd0cUpQbEFnN1RDeWx3Qmc&output=csv",\
	"axe":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHVuUEdLVmZzUE90SVU3Y3Mzc1FvSGc&output=csv", \
	"citypoly":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGhGcWloTXZ3Wm95akRJR0d6cW1JS2c&output=csv", \
	#"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHg4NTRKUU90cDZNczRxN0RVeEJDNXc&output=csv", \
	#"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFlmQ0NTU012Q192MW82X1dsLWgxTmc&output=csv", \
	"storyboard":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFYtWlMxTC1nM3l4aFFQeVJTamN4d2c&output=csv", \
	"anim_cinem":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdF81OVNPeGNCTHk4SklacGVKNHBldXc&output=csv", \
	"char_dev":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE5jVW9ldk9QOGt1ejlvM29SWksxT1E&output=csv",\
	"motiondesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE90aTV1V0h2X0FMM2RRVWtaNHBkNWc&output=csv", \
	"animation":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGlEWjNVYWM5VlcwcXZ6V3MydzB4Y3c&output=csv", \
	"animation_gallery":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDRJbnhOeFZOMjdSMWp1TmZzZVV4S2c&output=csv", \
	"motiondesign_gallery":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedHpTS0VGcmxoUnI4ckRwRHA1N2ZpdkE&output=csv", \
	"stbd_artists":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFdUaXc2VFFmcjVmNm0yWGpjMlNXRGc&output=csv", \
	"appdesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEduTXFac0d2eEh3T1pmS2cweFBzZ1E&output=csv", \
	"website":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGFLQk11cFNiRFFLODBBTWx1WlNYZWc&output=csv", \
	"touchscreen":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdG0tWVlNSW1jcS1pY3VXSC1ERFVUQnc&output=csv" \
	}

#
# Library...
#
import common

def get_dct( subset=None ):
	#print "SUBPAGE GETDCT"
	newdct = {}
	if subset==None: subset = SUB_PAGE_DEFS.keys()
	for code in subset:
		if not code in SUB_PAGE_DEFS.keys(): continue
		items = common.parse_spreadsheet1( SUB_PAGE_DEFS[code], "subpages->%s" % str(subset) )
		dct = common.dct_join( items,'subpage_key')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
