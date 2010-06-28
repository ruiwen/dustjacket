class EpubChapter:
	'''A single chapter in an EPub'''

	# The id used to reference this chapter as used in content.opf
	idref = ""
	
	# The file holding the contents of this EpubChapter
	# Expects a file-like object
	contentfile = None
	
	# Chapter label
	# Handy when displaying a "coverpage" for the chapter
	label = ""
	
	# Play order
	play_order = 0

	# Chapter contents from the contentfile
	__content = ""

	def __init__(self, epub, idref, play_order, contentfile, label=""):
		
		self.idref = idref
		self.play_order = play_order
		self.contentfile = contentfile
		self.label = label		

		self.__content = epub.open(contentfile).read()
		
		


			
			