#
# Configuration...
#
LOOKUP_FILE = "lookup.bin"

ASSET_PARENT_DIR = "../phil_assets/previsualization/storyboards-artists/"

CAPTION_PARENT_DIR = "../captions/Illustrators"

ILLUS_DIRS = [  ["andrew reid","Andrew"],
		["david lee","Dave"],
		["kurt komoda","Kurt"],
		["michael ocasio","michael"],
		["sarah chalek","Sarah"],
		["adrian mateescu","Adrian"],
		["anthony marte","Anthony"],
		["john holmes","John"],
		["matt buck","Matt"],
		["philomena marano","Philo"] ]

IGNORE_ASSETS = [ "matt19.png" ]

#
# Program...
#
import os
import sys
import pickle
import PIL
from PIL import Image

LOOKUP = None

def getnum(str):
	numstr = ""
	for c in str:
		if c=="-": break
		if c.isdigit(): numstr += c
	if (numstr==""): return -1
	return int(numstr)

def get_cap_file( file ):

	global LOOKUP
	if LOOKUP == None:
		LOOKUP = pickle.load( open( LOOKUP_FILE, "rb" ) )

	if LOOKUP.has_key(file):
		return LOOKUP[file]
	else:
		print "WARNING: No cap for->", file
		return None

def gen_lookup():

	lookup = {}

	# iterate asset dirs...
	for pair in ILLUS_DIRS:
		asset_dr = pair[0]
		dpath = os.path.join( ASSET_PARENT_DIR, asset_dr )
		asset_files = os.listdir(dpath)
	
		cap_dr = pair[1]
		dpath = os.path.join( CAPTION_PARENT_DIR, cap_dr )
		cap_files = os.listdir(dpath)

		# iterate assets files...	
		for file in asset_files:
			if ( file in IGNORE_ASSETS ): continue

			ii = getnum(file)
			if ii<0: continue
			idx = "%02d" % ii
			print ii, idx

			# locate its matching caption...
			found = None
			cap_files_cp = cap_files[:]
			for cap_file in cap_files_cp:
				if ( cap_file.find( idx ) >=0 ):
					cap_files_cp.remove( cap_file )
					found = cap_file
					break
			if found == None:
				print "ERROR: Could not find match for->", file, cap_files
				sys.exit(1)

			if lookup.has_key(file):
				print "ERROR: Already have->", file
				sys.exit(1)

			a = Image.open( os.path.join( CAPTION_PARENT_DIR, os.path.join( cap_dr, found ) ) )
			size = a.size
			width = size[0]
			height = size[1]

			lookup[file] = [ found, width, height ]

	return lookup

if __name__ == "__main__":

	lookup = gen_lookup()
	print lookup
	pickle.dump( lookup, open( LOOKUP_FILE, "wb" ) )
	print "wrote file->", LOOKUP_FILE

