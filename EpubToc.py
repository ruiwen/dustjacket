from Exceptions import BadEpubException
from EpubChapter import EpubChapter
from lxml import etree
import re
import json

class EpubToc:
	'''Represents the Table Of Contents of an Epub. Is a collection of EpubChapters'''	
	
	# The XML TOC
	__toc = None
	
	# Namespaces
	__namespaces = {}
	
	# Are we using the OEBPS system?
	__has_oebps = True
	
	# List of chapters
	chapters = []
	
	def __init__(self, epub, tocfile=None):
		'''Instantiates an EpubToc'''
		
		if not tocfile:
			try:
				try:
					tocfile = epub.open("OEBPS/toc.ncx") # Fallback on assumed defaults, that toc.ncx is in prescribed OEBPS/
				except KeyError:
					tocfile = epub.open("toc.ncx") # Fallback on assumed defaults, that toc.ncx is in root level
					self.__has_oebps = False
			except KeyError:
				raise BadEpubException("Unable to find toc.ncx")
		

		# We expect tocfile to be file-like object
		self.__toc = etree.parse(tocfile)
		
		# Get the TOC namespace
		self.__namespaces['ncx'] = self.__toc.getroot().nsmap[None]
		
		# Discover if this ePub has a dtb:generator tag..
		meta = self.__toc.find("//{%(tocns)s}meta[@name='dtb:generator']" % {'tocns': self.__namespaces['ncx']})
		
		# ... and if the generator was Calibre
		# It seems that Calibre currently generates ePubs that do not place content in OEBPS/, and have toc.ncx's 
		# that do not quite match <spine> in content.opf
		if meta is not None and re.match("calibre.+", meta.attrib['content']):
			self.__parse_calibre(epub)
		else:
			self.__parse_oebps(epub)
		
	
	def __parse_oebps(self, epub):
		'''Construct the chapter list assuming that the ePub has files in OEBPS/.'''

		# Parse the chapters
		npoints = self.__toc.findall("//{%(tocns)s}navPoint" % {'tocns': self.__namespaces['ncx']})
		for p in npoints:					
			#rt = p.getroottree()
			title = p.findtext("{%(tocns)s}text" % {'tocns': self.__namespaces['ncx']}) # Label text			
			contentfile = p.find("{%(tocns)s}content[@src]" % {'tocns':self.__namespaces['ncx']}).attrib['src'] # Contentfile name
			if self.__has_oebps:
				contentfile = "OEBPS/" + contentfile
				
			self.chapters.append(EpubChapter(epub, p.attrib['id'], p.attrib['playOrder'], contentfile, title))
		
	
	def __parse_calibre(self, epub):
		'''Special parsing mode for Calibre-generated ePubs that don't adhere to sticking files in OEBPS/.'''
		
		# This is an ugly hack, I'm sorry.
		# Calibre-generated ePubs seem to have toc.ncx's that are somewhat sparse, with <manifest> in content.opf more complete instead.
		# So let's parse <manifest>				
		#spine = epub.get_opf_data("spine") # Get the <spine> ElementTree
		manifest = epub.get_opf_data("manifest") # Get the <manifest> ElementTree
		
		ns = ""
		if manifest is not None:
			ns = manifest.getroot().nsmap[None]
		else:
			raise BadEpubException("Unable to namespace of ebook spine.")
			
			
		# Parse xhtml/xml items in the manifest
		items = manifest.findall("//{%(ns)s}item[@media-type='application/xhtml+xml']" % {'ns': ns})
		for idx, i in enumerate(items):
			self.chapters.append(EpubChapter(epub, i.attrib['id'], idx, i.attrib['href']))
		
		
	
	def get_chapter_titles(self):
		return [ c.contentfile for c in self.chapters ]
		
	