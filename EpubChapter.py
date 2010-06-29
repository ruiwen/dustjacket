from lxml import html

class EpubChapter:
	'''A single chapter in an EPub'''

	# The id used to reference this chapter as used in content.opf
	idref = ""
	
	# The name of the file holding the contents of this EpubChapter
	contentfile = ""
		
	# Play order
	play_order = 0

	# Chapter contents from the contentfile read as a HTML tree
	__content = None
	
	# List of paragraphs, each of an Element
	__paragraphs = []
	
	# Paragraph title
	title = ""

	def __init__(self, epub, idref, play_order, contentfile, title=""):
		
		self.idref = idref
		self.play_order = play_order
		self.contentfile = contentfile
		self.title = title	

		self.__content = html.parse(epub.open(contentfile))
		
		

	def __parse_paragraphs(self):
		'''Parse the Chapter's contents to derive a list of text paragraphs making up the Chapter.'''
		self.__paragraphs = self.__content.cssselect("p") # Select all the paragraphs via <p> tag
		
		# Attempt to derive the title of the Chapter, most often found in the first <h2> tag
		self.__title = self.__content.cssselect("h2")[0].text_content()
			
			