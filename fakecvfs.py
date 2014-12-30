#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import fuse
import stat
import time
import os

fuse.fuse_python_api = (0, 2)

class CVStat(fuse.Stat):
	"""
	Convenient class for Stat objects.
	Set up the stat object with appropriate
	values depending on constructor args.
	"""
	def __init__(self, is_dir, size):
		fuse.Stat.__init__(self)
		if is_dir:
			self.st_mode = stat.S_IFDIR | 0755
			self.st_nlink = 2
		else:
			self.st_mode = stat.S_IFREG | 0444
			self.st_nlink = 1
			self.st_size = size
		self.st_atime = 0
		self.st_mtime = 0
		self.st_ctime = 0

class FakeCVFS(fuse.Fuse):
	"""
	Class to emulate a filesystem that will ingest any file you trow at him
	It will return any file requested but the file will be predefined (/tmp/mockcv.doc)
	"""
	def __init__(self, *args, **kw):
		fuse.Fuse.__init__(self, *args, **kw)

	def getattr(self, path):
		if path == '/':
			is_dir=1
			size=1
		else:
			is_dir=0
			size=40960
		return CVStat(is_dir,size)

	def readdir(self, path, offset):
		for e in '.', '..', 'This is flat fake FS that will return any requested file. No dirs':
			yield fuse.Direntry(e)
	
	def read(self, path, size, offset):
		fh = open('/tmp/mockcv.doc', 'rb');
		data = fh.read()
		fsize = os.path.getsize('/tmp/mockcv.doc')
		if offset < fsize:
			if offset + size > fsize:
				size = fsize - offset
			return data[offset:offset+size]
		else:
			return ''

	def statfs(self):
		return os.statvfs('/')

if __name__ == '__main__':
	fs = FakeCVFS()
	fs.parse(errex=1)
	fs.main()
