from Exceptions import BadEpubException
from EpubToc import EpubToc
import zipfile
from lxml import etree

class Epub:
	# Wrapper class to manipulate ePub files
	# Does not currently support creation of ePub files from scratch, only reading/manipulation.

	# Internal reference to original filename
	__filename = ""
	
	# File reference pointer to original zip/epub file
	__epub = None
	
	# Store the various namespaces
	__namespaces = {}
	
	# OPF info - An lxml Element
	__opf = None
	
	# Table of Contents
	__toc = None

	def __init__(self, filename):
		# Initialiser.
		# Takes a filename and returns an EPub object if it's a valid ePub file
		# @params filename String Filename of the ePub to instantiate
		
		try:
			if zipfile.is_zipfile(filename):
				# Looks like we're valid! Time to get rolling
				
				self.__filename = filename
				self.__epub = zipfile.ZipFile(filename, 'a')		
									
			else:
				raise BadEpubException("%(filename)s seems like an invalid ePub. It is not a ZIP file." % {"filename": filename})
				
		except BadEpubException as e:	
			print unicode(e)


	def __read_opf(self):

		# Find the "content.opf" file - "META-INF/container.xml" is a fixed location
		container = etree.parse(self.__epub.open("META-INF/container.xml"))
		self.__namespaces['container'] = container.getroot().nsmap[None]
		opfname = container.find("//{%(ns)s}rootfile" % {'ns':self.__namespaces['container']}).attrib['full-path']		
		
		#Find the opf file discovered above
		if opfname in self.__epub.namelist():
			self.__opf = etree.parse(self.__epub.open(opfname)).getroot()
		else:
			raise BadEpubException("%(filename)s doesn't seem like a valid ePub file. Unable to determine ePub's meta info." % {"filename":filename})
	
		# Get the default namespace
		try:				
			self.__namespaces['opf'] = {'package': self.__opf.nsmap[None]}
		except KeyError:
			self.__namespaces['opf'] = {'package': self.__opf.nsmap['opf']}
		except AttributeError as e:
			raise BadEpubException("%(filename)s doesn't seem like a valid ePub file. Unable to determine default namespace." % {'filename':filename})			


	def __read_toc(self):
		'''Construct the table of contents for this epub'''
		self.__toc = EpubToc(self)
	
	
	def open(self, name, **kwargs):
		'''Epub.open() masquerades and passes through to the original epub zipfile.'''
		# I'm not quite sure if this is a good idea, but here goes anyway...
		return self.__epub.open(name, **kwargs)
	
	
	def get_opf_data(self, tag):
		'''Returns the ElementTree in the OPF file that matches the tag specified.'''
		
		if self.__opf is None: # Make sure self.__opf exists
			self.__read_opf()
		
		try:		
			return self.__opf.getroottree().find("//{%(opfns)s}%(tag)s" % {'opfns': self.__namespaces['opf']['package'], 'tag':tag }).getroottree()
		except AttributeError:
			return None
	

	def get_metainfo(self, info):
		# Retrieve metainformation from the ePub
		
		# 'package' is the root element of the OPF info, so we check if we have that
		if not self.__namespaces.has_key('opf') or not self.__namespaces['opf'].has_key('package') or self.__namespaces['opf']['package'] != "":
			self.__read_opf()

		if not self.__namespaces['opf'].has_key('dc') or self.__namespaces['opf']['dc'] == "":
			# Get the 'metadata' element's namespace. At least enough for us to do our job of retrieving the info
			meta = self.__opf.find("{%(packagens)s}metadata" % {'packagens':self.__namespaces['opf']['package']} )
			self.__namespaces['opf'].update({'dc': meta.nsmap['dc']})

		# Retrieve the information
		return meta.findtext("{%(dcns)s}%(info)s" % {'dcns': self.__namespaces['opf']['dc'], 'info': info})
		
	
	@property
	def creator(self):
		# Convenience method/attribute equivalent to self.get_metainfo('creator')
		return self.get_metainfo("creator")
	
	@property
	def title(self):
		# Convenience method/attribute equivalent to self.get_metainfo('title')
		return self.get_metainfo("title")
	

	@property
	def identifier(self):
		# Convenience method/attribute equivalent to self.get_metainfo('identifier')
		return self.get_metainfo("identifier")
	
	
	@property
	def publisher(self):
		# Convenience method/attribute equivalent to self.get_metainfo('publisher')		
		return self.get_metainfo("publisher")	


	@property
	def toc(self):
		if not self.__toc:
			self.__read_toc()
			
		return self.__toc

	
	def get_namespace(self, name):

		# Attempts to return the requested namespace for this ePub, if available. Returns "" otherwise
		if self.__namespaces.has_key(name):
			return self.__namespaces[name]
		else:
			return ""


	def __str__(self):
		return self.filename

	def __unicode__(self):
		return "%(title)s - %(creator)s - %(identifier)" % {'title':self.title, 'creator':self.creator, 'identifier':self.identifier}


			
		