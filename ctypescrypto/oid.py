"""	
 Interface to OpenSSL object identifier database.

 It is primarily intended to deal with OIDs which are compiled into the
 database or defined in the openssl configuration files.

 But see create() function

"""
from ctypescrypto import libcrypto
from ctypes import c_char_p, c_void_p, c_int, create_string_buffer

__all__ = ['Oid','create','cleanup']

class Oid(object):
	"""
		Represents an OID. It can be consturucted by textual
		representation like Oid("commonName") or Oid("CN"),
		dotted-decimal Oid("1.2.3.4") or using OpenSSL numeric
		identifer (NID), which is typically returned or required by 
		OpenSSL API functions. If object is consturcted from textual
		representation which is not present in the database, it fails
		with ValueError

		attribute nid - contains object nid.


	"""

	def __init__(self,value):
		" Object constuctor. Accepts string or integer"
		if type(value) == type(""):
			self.nid=libcrypto.OBJ_txt2nid(value)
			if self.nid==0:
				raise ValueError("Cannot find object %s in the database"%(value))
		elif type(value) == type(0):
			cn=libcrypto.OBJ_nid2sn(value)
			if cn is None:
				raise ValueError("No such nid %d in the database"%(value))
			self.nid=value
		else:
			raise TypeError("Cannot convert this type to object identifier")
	def __hash__(self):
		" Returns NID "
		return self.nid
	def __cmp__(self,other):
		" Compares NIDs of two objects "
		return self.nid-other.nid
	def __str__(self):
		" Default string representation of Oid is dotted-decimal"
		return self.dotted()
	def __repr__(self):
		return "Oid('%s')"%(self.dotted())
	def shortname(self):
		" Returns short name if any "
		return libcrypto.OBJ_nid2sn(self.nid)
	def longname(self):
		" Returns logn name if any "
		return	libcrypto.OBJ_nid2ln(self.nid)
	def dotted(self):
		" Returns dotted-decimal reperesentation "
		obj=libcrypto.OBJ_nid2obj(self.nid)
		buf=create_string_buffer(256)
		libcrypto.OBJ_obj2txt(buf,256,obj,1)
		return buf.value
	@staticmethod
	def fromobj(obj):
		"""
		Creates an OID object from the pointer to ASN1_OBJECT c structure.
		Strictly for internal use
		"""
		nid=libcrypto.OBJ_obj2nid(obj)
		if nid==0:
			buf=create_string_buffer(80)
			l=libcrypto.OBJ_obj2txt(buf,80,obj,1)
			oid=create(buf[0:l],buf[0:l],buf[0:l])
		else:
			oid=Oid(nid)
		return oid

def create(dotted,shortname,longname):
	"""
		Creates new OID in the database

		@param dotted - dotted-decimal representation of new OID
		@param shortname - short name for new OID
		@param longname - long name for new OID

		@returns Oid object corresponding to new OID
		
		This function should be used with exreme care. Whenever
		possible, it is better to add new OIDs via OpenSSL configuration
		file

		Results of calling this function twice for same OIDor for
		Oid alredy in database are undefined
	"""
	nid=libcrypto.OBJ_create(dotted,shortname,longname)
	if nid == 0:
		raise LibCryptoError("Problem adding new OID to the  database")
	return Oid(nid)

def cleanup():
	"""
		Removes all the objects, dynamically added by current
		application from database.
	"""
	libcrypto.OBJ_cleanup()

libcrypto.OBJ_nid2sn.restype=c_char_p
libcrypto.OBJ_nid2ln.restype=c_char_p
libcrypto.OBJ_nid2obj.restype=c_void_p
libcrypto.OBJ_obj2txt.argtypes=(c_char_p,c_int,c_void_p,c_int)
libcrypto.OBJ_txt2nid.argtupes=(c_char_p,)
libcrypto.OBJ_create.argtypes=(c_char_p,c_char_p,c_char_p)
