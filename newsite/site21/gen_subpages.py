#
# Configuration...
#

#SUB_PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEllOHZqalNfSlFCaF9oYXF6a3pqTGc&output=csv"

SUB_PAGE_DEFS = { "home":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFpwVkZzOW5zTTF1QTZzNkFuUjFodkE&output=csv", \
	"whoweare":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEptTWZNbG5ZVTI0ZWU4bDluaVNpWHc&output=csv", \
	"sneakpeek":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE5xR2tvbUl0VEFsZFgzRVVhazR2Q1E&output=csv", \
	"clients":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGRZMTN0b1ZBZ3BiN0ktbDg0X3EyUGc&output=csv", \
	"contacts":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHU2dGVKWXdLckQxQTZXWFpJZ3kyZ3c&output=csv", \
	"community":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGJRcnZvck00R0dIRXZuYkJDVm5iM3c&output=csv", \
	"map":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDhzajRpU1JsdlZ2amFyMGlMekw4a2c&output=csv", \
	"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGpJM1FEVGg3RVhaTHJjcFRwVEtsQXc&output=csv", \
	"photos":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpGaC1Xam5xeFR1MGpwc05aYU1YZlE&output=csv", \
	"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFhUTFlOQjVqR0VwRVg4UW9YeGc1d1E&output=csv", \
	"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHg4NTRKUU90cDZNczRxN0RVeEJDNXc&output=csv" }

#
# Library...
#
import common

def get_dct( subset=None ):

	newdct = {}
	if subset==None: subset = SUB_PAGE_DEFS.keys()
	for code in subset:
		items = common.parse_spreadsheet1( SUB_PAGE_DEFS[code] )
		print "SPD->",items
		dct = common.dct_join( items,'subpage_key')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
