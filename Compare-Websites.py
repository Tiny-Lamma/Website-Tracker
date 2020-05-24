#!/usr/bin/python3

import sys
import difflib

def main(filenames):
	if len(sys.argv) != 3:
		print('USAGE: \nWebsite-Diff.py filename filename')

	text1 = open(filenames[0]).readlines()
	text2 = open(filenames[1]).readlines()

	for line in difflib.unified_diff(text1, text2):
	    print(line)

if __name__ == "__main__":
	if len(sys.argv) != 3:
        	print('USAGE: \n\tWebsite-Diff.py filename filename')
	else:
		main(sys.argv[1:])
