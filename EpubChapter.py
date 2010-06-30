from lxml import html
import json

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
		
		cr = self.__content.getroot() # Get the content root Element
		
		self.__paragraphs = cr.cssselect("p") # Select all the paragraphs via <p> tag
		
		# Attempt to derive the title of the Chapter, most often found in the first <h2> tag
		# It's a rough heuristic to determine the chapter title, but hey, something is better than nothing
		if self.title == "":
			self.title = cr.cssselect("h2")[0].text_content()
			
			
	
	def get_original_text(self):
		'''Returns the original HTML content of a Chapter'''
		if self.__content is not None:
			return html.tostring(self.__content)
		else:
			return ""

						
			
	def get_paragraph_text(self, full_body=False):
		'''Returns a long string comprising the HTML making up the paragraphs of the chapter, wrapped in <p> tags, delineated by newline characters.'''
		out = []
		
		if not self.__paragraphs:
			self.__parse_paragraphs()
		
		for p in self.__paragraphs:
			out.append(html.tostring(p))		
					
		fragment = html.fragment_fromstring(u"\n".join(out), create_parent='div') # Wrap the <p>'s in a <div>
		
		if full_body:
			return html.tostring(html.document_fromstring(html.tostring(fragment)))
		else:
			return html.tostring(fragment)