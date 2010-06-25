import zipfile

class EPub:
	# Wrapper class to manipulate ePub files
	# Does not currently support creation of ePub files from scratch, only reading/manipulation.

	# Internal reference to original filename
	filename = ""
	
	# Internal reference to ZipFile Object from given ePub
	zipfile = None

	def __init__(self, filename):
		# Initialiser.
		# Takes a filename and returns an EPub object if it's a valid ePub file
		# @params filename String Filename of the ePub to instantiate
		
		try:
			if zipfile.is_zipfile(filename):
				# Looks like we're valid! Time to get rolling
				
				self.filename = filename
				self.zipfile = zipfile.ZipFile(filename, 'a')
				
				
			else:
				raise BadEpubException("%(filename)s seems like an invalid ePub. It is not a ZIP file." % {"filename": filename})
				
		except BadEpubException as e:	
			print unicode(e)

	
	def 


	def __str__(self):
		return self.filename

	def __unicode__(self):
		return self.filename


class BadEpubException(Exception):
	pass

#	# Copied from http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
#    def __init__(self, message, Errors):
#	
#	    # Call the base class constructor with the parameters it needs
#	    Exception.__init__(self, message)
#	
#	    # Now for your custom code...
#	    self.Errors = Errors
			
		