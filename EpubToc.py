from Exceptions import BadEpubException
from EpubChapter import EpubChapter
from lxml import etree

class EpubToc:
	'''Represents the Table Of Contents of an Epub. Is a collection of EpubChapters'''	
	
	# The XML TOC
	__toc = None
	
	# Namespaces
	__namespaces = {}
	
	# List of chapters
	chapters = []
	
	def __init__(self, epub, tocfile=None):
		'''Instantiates an EpubToc'''
		
		has_oebps = False
		
		if not tocfile:
			try:
				try:
					tocfile = epub.open("OEBPS/toc.ncx") # Fallback on assumed defaults, that toc.ncx is in prescribed OEBPS/
					has_oebps = True # Set a flag here so that we know to adjust the paths accordingly later
				except KeyError:
					tocfile = epub.open("toc.ncx") # Fallback on assumed defaults, that toc.ncx is in root level
			except KeyError:
				raise BadEpubException("Unable to find toc.ncx")
		

		# We expect tocfile to be file-like object
		self.__toc = etree.parse(tocfile)
		
		# Get the TOC namespace
		self.__namespaces['ncx'] = self.__toc.getroot().nsmap[None]
		
		# Parse the chapters
		npoints = self.__toc.findall("//{%(tocns)s}navPoint" % {'tocns': self.__namespaces['ncx']})
		for p in npoints:
		
			rt = p.getroottree()
			l = rt.findtext("//{%(tocns)s}text" % {'tocns': self.__namespaces['ncx']}) # Label text			
			c = rt.find("//{%(tocns)s}content" % {'tocns':self.__namespaces['ncx']}).attrib['src'] # Content
			if has_oebps:
				c = "OEBPS/" + c
				
			self.chapters.append(EpubChapter(epub, p.attrib['id'], p.attrib['playOrder'], c, l))
	
		
		
		
	