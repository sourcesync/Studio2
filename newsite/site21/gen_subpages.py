#
# Configuration...
#

#SUB_PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEllOHZqalNfSlFCaF9oYXF6a3pqTGc&output=csv"

SUB_PAGE_DEFS = { "home":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFpwVkZzOW5zTTF1QTZzNkFuUjFodkE&output=csv", \
	"whoweare":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEptTWZNbG5ZVTI0ZWU4bDluaVNpWHc&output=csv", \
	"sneakpeek":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdE5xR2tvbUl0VEFsZFgzRVVhazR2Q1E&output=csv" }

#
# Library...
#
import common

def get_dct():

	newdct = {}
	for code in SUB_PAGE_DEFS.keys():
		items = common.parse_spreadsheet1( SUB_PAGE_DEFS[code] )
		print "SPD->",items
		dct = common.dct_join( items,'subpage_key')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
