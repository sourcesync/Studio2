#
# Configuration...
#

SUB_PAGE_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEllOHZqalNfSlFCaF9oYXF6a3pqTGc&output=csv"

#
# Library...
#
import common

def get_dct():
	items = common.parse_spreadsheet1( SUB_PAGE_DEF )
	dct = common.dct_join( items,'subpage_key')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct
