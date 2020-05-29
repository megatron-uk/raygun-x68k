#!/usr/bin/env python3

import getopt
import os
import sys
import traceback
from shutil import copyfile

from text import text_lookup

# Where scripts are kept, by default
SCRIPT_DIR = "csv/disk1"

def title():
	print("%s - Script injector for Ray-Gun (X68000 version)" % __file__)
	print("")

def help():
	""" Show command line use """

	title()
	print("-v --verbose 	Enable extra debug output")
	print("-s --script	Name of script file to parse")
	print("-d --dir	Directory where your Ray-Gun data files are located")
	print("")
	print("e.g.")
	print("inject.py -s START.MES -d /tmp/ray-gun")
	print("")
	print("Uses the translated script file START.MES in csv/disks/ and patches")
	print("the relevant data file found in /tmp/ray-gun. Note: the original data")
	print("will be renamed as START.MES.orig")

def decode_options():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "vhs:d:", ["help", "verbose", "script=", "dir="])
	except getopt.GetoptError as err:
		print(str(err))
		help()
		sys.exit(2)

	script = None
	data_dir = None
	verbose = False
	
	for o, a in opts:
		if o in ("-v", "--verbose"):
			verbose = True
		elif o in ("-h", "--help"):
			help()
			sys.exit()
		elif o in ("-s", "--script"):
			script = a
		elif o in ("-d", "--dir"):
			data_dir = a
		else:
			assert False, "unhandled option"

	if (script is None) or (data_dir is None):
		help()
		print("")
		print("ERROR: You must supply both a script name and a data directory path")
		print("")
		sys.exit()
		
	r = patcher(script = script, data_dir = data_dir, verbose = verbose)
	if r:
		sys.exit(0)
	else:
		sys.exit(1)

def patcher(script = None, data_dir = None, verbose = False):
	""" Runs the patching script """
	
	title()
	
	script_path = SCRIPT_DIR + "/" + script + ".csv"
	if os.path.isfile(script_path):
		print("Using script:	%s" % script_path)
	else:
		print("")
		print("ERROR: The script %s does not exist" % script_path)
		print("")
		return False
		
	if os.path.exists(data_dir):
		print("Using game dir:	%s" % data_dir)
	else:
		print("")
		print("ERROR: The game data dir %s does not exist" % data_dir)
		print("")
		return False
		
	data_path = data_dir + "/" + script
	if os.path.isfile(data_path):
		print("Found:	 	%s" % data_path)
	else:
		print("")
		print("ERROR: The game data file %s does not exist" % data_path)
		print("")
		return False
		
	script_size = 0
	script_hex = 0
	script_eng_text = 0
	script_jpn_text = 0
	script_lines = []
	script_start = 0x0
	
	print("")
	print("Parsing script...")
	
	f = open(script_path, "r")
	fields = []
	script_line = {}
	try:
		c = 0
		for l in f:
												
			# Only start after the header row
			if c > 0:
				fields = l.split(";")
				script_line = {
					'script_file' : fields[0],
					'script_idx' : int(fields[1]),
					'script_pos' : fields[2],
					'script_ishex' : fields[3],
					'script_orig' : fields[4],
					'script_trans' : fields[5],
					'script_final' : fields[6],
					'script_line_width' : int(fields[7].replace('\n', ''))
				}

				# Ensure that the file is valid and doesnt contain data for another game resource
				if script_line['script_file'].lower() !=  script.lower():
					print("ERROR: Error on line %s" % c)
					print("ERROR: This script is for data file [%s], NOT [%s]!" % (script_line['script_file'], script))
					print("")
					return False
				
				script_lines.append(script_line)
				
				# Update counters
				if script_line['script_ishex'] == "Y":
					script_hex += 1
				else:
					if len(script_line['script_final']) > 0:
						script_eng_text += 1
					else:
						script_jpn_text += 1
					
				# Row 1 contains the byte position of the first insertion
				if c == 1:
					script_start = int(script_line['script_pos'], 16)
					
			# Increment row counter
			c+= 1
			
		script_size = len(script_lines)
		f.close()
		print("Done")
	except Exception as e:
		print("ERROR: Unable to parse script")
		print("The error was: %s" % e)
		print("Fields: %s" % fields)
		print("Script Line: %s" % script_line)
		return False
	
	if verbose:
		print("")
		print("Script start position:	%s" % hex(script_start))
		print("Script total lines:	%s" % script_size)
		print("- Hex codes:		%s" % script_hex)
		print("- English:		%s" % script_eng_text)
		print("- Japanese:		%s" % script_jpn_text)
		
	print("")
	print("Archiving %s to %s" % (data_path, data_path + ".orig"))
	print("Archiving %s to %s" % (data_path, data_path + ".new"))
	try:
		copyfile(data_path, data_path + ".orig")
		copyfile(data_path, data_path + ".new")
		print("Done")
	except Exception as e:
		print("ERROR: Unable to archive data file")
		print("The error was: %s" % e)
		return False
	
	# Open data_path + ".new"#
	if verbose:
		print("")
		print("Opening %s.new for writing" % data_path)
	try:
		output_file = open(data_path + ".new", "wb")
	except Exception as e:
		print("ERROR: Unable to open file for writing")
		print("The error was: %s" % e)
		return False
	
	# Seek to script_start
	if verbose:
		print("Seeking to %s" % hex(script_start))
	output_file.seek(script_start, 0)
	
	supported_chars = text_lookup.keys()
	for line in script_lines:
		try:
			# If hex - insert bytes
			if line['script_ishex'].upper() == "Y":
				if verbose:
					print("%s - Hex bytes" % line['script_idx'])
					
				hex_bytes = line['script_orig'].rstrip().lstrip().split(' ')
				line_text = []
				for h in hex_bytes:
					line_text.append(int(h, 16))
				line_bytes = bytes(line_text)
				#if verbose:
				#	print("%s - [%s]" % (line['script_idx'], line_bytes))
				output_file.write(line_bytes)
			# else
			else:
				# if script_final > 0 convert to sjis and insert
				if len(line['script_final']) > 0:
					line_text = line['script_final']
					line_print = line_text
					line_type = "translated"
					
				# else convert machine translated to sjis and insert
				else:
					line_text = line['script_trans']
					line_print = line_text
					line_type = "literal"	
				
				new_line_text = ""
				c = 0
				for ch in line_text:
					# If we reach the display limit of the line, embed a return
					# and carry on with the next character
					if (c % line['script_line_width'] == 0) and (c != 0):
						new_line_text += "|"
						# Skip a trailing space after a carriage return
						if ch != " ":
							# Add next character
							new_line_text += ch
					else:
						# Add next character
						new_line_text += ch
					c += 1
				line_text = new_line_text
				if verbose:
					if line_type == "literal":	
						print("%s - <raw> %s" % (line['script_idx'], line_text))
					else:
						print("%s - <ok!> %s" % (line['script_idx'], line_text))
					
				# Output the characters in 'line_text'
				line_bytes = []
				for c in line_text:
					if c in supported_chars:
						b1 = text_lookup[c][0]
						line_bytes.append(b1)
						if len(text_lookup[c]) > 1:
							b2 = text_lookup[c][1]
							line_bytes.append(b2)
					else:
						print("ERROR: Unsupported character in output line %s!" % line['script_idx'])
						print("The character was: [%s]" % c)
						return False
						
				#if verbose:
				#	print("%s - [%s]" % (line['script_idx'], line_bytes))
				
				output_file.write(bytes(line_bytes))
		except Exception as e:
			print("ERROR: Unable to write line %s to output file" % line['script_idx'])
			print("The error was: %s" % e)
			print("The traceback was: %s" % traceback.format_exc())
			return False
	
	# close file
	output_file.close()

if __name__ == "__main__":
    decode_options()