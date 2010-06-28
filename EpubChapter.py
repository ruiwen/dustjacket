from lxml import html

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

	# Chapter contents from the contentfile read as a HTML tree
	__content = None
	
	# List of paragraphs, each of an Element
	__paragraphs = []
	

	def __init__(self, epub, idref, play_order, contentfile, label=""):
		
		self.idref = idref
		self.play_order = play_order
		self.contentfile = contentfile
		self.label = label		

		self.__content = html.parse(epub.open(contentfile))
		
		

	def __parse_paragraphs(self):
		'''Parse the Chapter's contents to derive a list of text paragraphs making up the Chapter.'''
		self.__paragraphs = self.__content.cssselect("p") # Select all the paragraphs via <p> tag
		
		
			
			