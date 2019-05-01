# Parser - Dominick Aiudi
# This program will read from a text file and
# pass associated images' locations
# 
# Currently used for the background

import pygame
import random
import GameBase
import configparser  # Class for parsing


# Main currently will pull and parse file

def main(pos, length, width):
	# initalization
	rows = []
	tileset = []
	config = configparser.ConfigParser()
	config.read('map.txt')

	# pick background based on positioning
	if (pos.y == 0):
		# NW corner
		if (pos.x == 0):
			rows = config.get('BG', 'c_NW').split('\n')
		# NE corner
		elif (pos.x == (width - 1)):
			rows = config.get('BG', 'c_NE').split('\n')
		# N edge
		else:
			rows = config.get('BG', 'ed_N').split('\n')
	elif (pos.y == (length - 1)):
		# SW corner
		if (pos.x == 0):
			rows = config.get('BG', 'c_SW').split('\n')
		# SE corner
		elif (pos.x == (width - 1)):
			rows = config.get('BG', 'c_SE').split('\n')
		# S edge
		else:
			rows = config.get('BG', 'ed_S').split('\n')
	# W edge
	elif (pos.x == 0):
		rows = config.get('BG', 'ed_W').split('\n')
	# E edge
	elif (pos.x == (width - 1)):
		rows = config.get('BG', 'ed_E').split('\n')
	# Not an edge
	else:
		rows = config.get('BG', 'op_N').split('\n')

	tileset = addRow(tileset, rows)

	return tileset # Return list of a list of strings
	#
	# tileset looks something like this:
	# tileset[0] = [".", ".", ... "."] for 9 characters
	# .
	# .
	# .
	# tileset[8] = [".", ".", ... "."]
	#

def addRow(lis_tileset, lis_rows):
	for row in lis_rows:
		lis_tileset.append(list(row))
	return lis_tileset


# Get dictionary of character to image file references
def tileDict():
	tileset = {}
	config = configparser.ConfigParser()
	config.read('map.txt')
	for key in config['Tiles']:
		tileset[key] = config['Tiles'][key]
	return tileset # Return dictionary of {string : string}
	#
	# tileset looks something like this:
	# tileset = {'.' = 'res/whatever.png', ...}
	#


def getLayout(roomType):
	rows = []
	tileset = []
	config = configparser.ConfigParser()
	config.read('map.txt')

	# pick room layout to use
	if roomType is GameBase.RoomType.NORMAL:
		rows = config.get('LAYOUT', str(random.choice(['sn_', 'hr_']) 
									+ str(random.randint(1,4)))).split('\n')
	else:
		row = config.get('LAYOUT', 'em_0').split('\n')

	tileset = addRow(tileset, rows)
	return tileset

def getLayoutLib():
	tileset = {}
	config = configparser.ConfigParser()
	config.read('map.txt')
	for key in config['Stuff']:
		tileset[key] = config['Stuff'][key]
	return tileset

if __name__ == "__main__" :
	main()
