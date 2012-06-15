
URL = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDBBVmpmNVpoRTQwVXZIR1ExQUk0bkE&output=csv"

import common

def gen_items():
	# get a list of items ( each a dct )...
	parsed = common.parse_spreadsheet1( URL )
     	return parsed 

if __name__=="__main__":
	items = gen_items()
	print items	
