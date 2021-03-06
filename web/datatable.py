# Need to install Pypi package "termcolor" for this
try:
    from termcolor import colored
except:
    pass


# data is a list of objects
# cols is a list of object members to be displayed
# colormap needs to be fixed
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
				row += " "+ str(vars(m)[col.strip()]).rjust(colpadding[col])
			except:
				row += " " + ''.rjust(colpadding[col]) 
	
		try:
			print colored(row, colormap[str(m.betresult)])
		except:
			print row
		row = ''
