#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modified from 'The Python Standard Library'
13.1. csv — CSV File Reading and Writing
http://docs.python.org/2/library/csv.html
"""

import csv, codecs
from io import StringIO


class UTF8Recoder:
	"""
	Iterator that reads an encoded stream and reencodes the input to UTF-8
	"""
	def __init__(self, f, encoding):
		self.reader = codecs.getreader(encoding)(f)

	def __iter__(self):
		return self

	def __next__(self):
		return next(self.reader).encode("utf-8")

class UnicodeReader:
	"""
	A CSV reader which will iterate over lines in the CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel,encoding="utf-8", delimiter="\t", **kwds):
		# f = UTF8Recoder(f, encoding)
		def fix_nulls(s):
		    for line in s:
		        yield line.replace('\0', ' ')
		self.reader = csv.reader(fix_nulls(f),dialect=dialect, delimiter=delimiter, **kwds)

	def __next__(self):
		row = next(self.reader)
		return [s for s in row]

	def __iter__(self):
		return self

class UnicodeWriter:
	"""
	A CSV writer which will write rows to CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel, encoding="utf-8", delimiter="\t", **kwds):
		# Redirect output to a queue
		self.queue = StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, delimiter=delimiter, **kwds)
		self.stream = f
		# self.encoder = codecs.getincrementalencoder(encoding)()

	def writerow(self, row):
		self.writer.writerow([s for s in row]) #.encode("utf-8") will create all string with b'
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		# ... and reencode it into the target encoding
		# data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)
