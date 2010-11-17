# Need to install Pypi package "termcolor" for this
from termcolor import colored

def datatable(data, cols, colormap={}):
	# Output the datatable
	row = ''
	colpadding = {}
	
	for col in cols:
		colpadding[col] = len(col)
	
	print " " + " ".join(cols)
	for m in data:
		for col in cols:
			try:
				row += " "+ str(vars(m)[col]).rjust(colpadding[col])
			except:
				row += " " + ''.rjust(colpadding[col]) 
	
		try:
			print colored(row, colormap[str(m.betresult)])
		except:
			print row
		row = ''
