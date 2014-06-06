from ctypescrypto.oid import Oid
from ctypescrypto import digest
from base64 import b16decode,b16encode
import unittest

class TestDigestType(unittest.TestCase):
	def test_md4(self):
		d=digest.DigestType("md4")
		self.assertEqual(d.digest_size(),16)
		self.assertEqual(d.block_size(),64)
		self.assertEqual(d.oid(),Oid("md4"))
	def test_md5(self):
		d=digest.DigestType("md5")
		self.assertEqual(d.digest_size(),16)
		self.assertEqual(d.block_size(),64)
		self.assertEqual(d.oid(),Oid("md5"))
	def test_sha1(self):
		d=digest.DigestType("sha1")
		self.assertEqual(d.digest_size(),20)
		self.assertEqual(d.block_size(),64)
		self.assertEqual(d.oid(),Oid("sha1"))
	def test_sha256(self):
		d=digest.DigestType("sha256")
		self.assertEqual(d.digest_size(),32)
		self.assertEqual(d.block_size(),64)
		self.assertEqual(d.oid(),Oid("sha256"))
	def test_sha384(self):
		d=digest.DigestType("sha384")
		self.assertEqual(d.digest_size(),48)
		self.assertEqual(d.block_size(),128)
		self.assertEqual(d.oid(),Oid("sha384"))
	def test_sha512(self):
		d=digest.DigestType("sha512")
		self.assertEqual(d.digest_size(),64)
		self.assertEqual(d.block_size(),128)
		self.assertEqual(d.oid(),Oid("sha512"))
		

class TestIface(unittest.TestCase):
	""" Test all methods with one algorithms """
	def test_cons(self):
		md=digest.DigestType("sha1")
		dgst=digest.Digest(md)
		dgst.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(dgst.digest_size,20)
		self.assertEqual(dgst.hexdigest(),"00CFFE7312BF9CA73584F24BDF7DF1D028340397")
	def test_bindigest(self):
		dgst=digest.new("sha1")
		dgst.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(dgst.digest_size,20)
		self.assertEqual(dgst.digest(),b16decode("00CFFE7312BF9CA73584F24BDF7DF1D028340397",True)) 
	def test_duplicatedigest(self):
		dgst=digest.new("sha1")
		dgst.update("A quick brown fox jumps over the lazy dog.")
		v1=dgst.digest()
		v2=dgst.digest()
		self.assertEqual(v1,v2)
	def test_copy(self):
		dgst=digest.new("sha1")
		dgst.update("A quick brown fox jumps over ")
		d2=dgst.copy()
		dgst.update("the lazy dog.")
		value1=dgst.hexdigest()
		d2.update("the fat pig.")
		value2=d2.hexdigest()
		self.assertEqual(value1,"00CFFE7312BF9CA73584F24BDF7DF1D028340397")
		self.assertEqual(value2,"5328F33739BEC2A15B6A30F17D3BC13CC11A7C78")
class TestAlgo(unittest.TestCase):
	""" Test all statdard algorithms """
	def test_md5(self):
		d=digest.new("md5")
		self.assertEqual(d.digest_size,16)
		d.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(d.hexdigest(),"DF756A3769FCAB0A261880957590C768")

	def test_md4(self):
		d=digest.new("md4")
		d.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(d.digest_size,16)
		self.assertEqual(d.hexdigest(),"FAAED595A3E38BBF0D9B4B98021D200F")
	def test_sha256(self):
		d=digest.new("sha256")
		d.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(d.digest_size,32)
		self.assertEqual(d.hexdigest(),"FFCA2587CFD4846E4CB975B503C9EB940F94566AA394E8BD571458B9DA5097D5")
	def test_sha384(self):
		d=digest.new("sha384")
		d.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(d.digest_size,48)
		self.assertEqual(d.hexdigest(),"C7D71B1BA81D0DD028E79C7E75CF2F83169C14BA732CA5A2AD731151584E9DE843C1A314077D62B96B03367F72E126D8")
	def test_sha512(self):
		d=digest.new("sha512")
		self.assertEqual(d.digest_size,64)
		d.update("A quick brown fox jumps over the lazy dog.")
		self.assertEqual(d.hexdigest(),"3045575CF3B873DD656F5F3426E04A4ACD11950BB2538772EE14867002B408E21FF18EF7F7B2CAB484A3C1C0BE3F8ACC4AED536A427353C7748DC365FC1A8646")

if __name__ == "__main__":
	unittest.main()