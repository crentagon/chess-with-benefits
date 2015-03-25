import os, sys, inspect

# Include folder modules
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

# Include subfolder modules
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

# Source: http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path