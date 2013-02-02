#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import ConfigParser
import logging

from utf8_utils import UnicodeReader
from api_utils import ModelAPI

class ImportStmt( object ):
	
	"""
	Copies STMT file formats into Termite internal format.
	"""
	
	# Files generated by STMT
	TERM_INDEX = 'term-index.txt'
	TOPIC_INDEX = 'topic-index.txt'
	DOCUMENT_INDEX = 'doc-index.txt'
	TOPIC_TERM = 'topic-term-distributions.csv'
	DOCUMENT_TOPIC = 'document-topic-distributions.csv'
	
	def __init__( self, logging_level ):
		self.logger = logging.getLogger( 'ImportStmt' )
		self.logger.setLevel( logging_level )
		handler = logging.StreamHandler( sys.stderr )
		handler.setLevel( logging_level )
		self.logger.addHandler( handler )
	
	def execute( self, model_library, model_path, data_path ):
		
		assert model_library is not None
		assert model_library == 'stmt'
		assert model_path is not None
		assert data_path is not None
		
		self.logger.info( '--------------------------------------------------------------------------------' )
		self.logger.info( 'Importing an STMT model...'                                                       )
		self.logger.info( '    topic model = %s (%s)', model_path, model_library                             )
		self.logger.info( '    output = %s', data_path                                                       )
		
		self.logger.info( 'Connecting to data...' )
		self.model = ModelAPI( data_path )
		
		self.logger.info( 'Reading "%s" from STMT output...', ImportStmt.TERM_INDEX )
		self.model.term_index  = self.readAsList( model_path, ImportStmt.TERM_INDEX )
		self.model.term_count = len(self.model.term_index)
		
		self.logger.info( 'Reading "%s" from STMT output...', ImportStmt.TOPIC_INDEX )
		self.model.topic_index = self.readAsList( model_path, ImportStmt.TOPIC_INDEX )
		self.model.topic_count = len(self.model.topic_index)
		
		self.logger.info( 'Reading "%s" from STMT output...', ImportStmt.DOCUMENT_INDEX )
		self.model.document_index = self.readAsList( model_path, ImportStmt.DOCUMENT_INDEX )
		self.model.document_count = len(self.model.document_index)
		
		self.logger.info( 'Reading "%s" from STMT output...', ImportStmt.TOPIC_TERM )
		self.topic_term_counts = self.readCsvAsMatrixStr( model_path, ImportStmt.TOPIC_TERM )
		
		self.logger.info( 'Reading "%s" from STMT output...', ImportStmt.DOCUMENT_TOPIC )
		self.document_topic_counts = self.readCsvAsMatrixStr( model_path, ImportStmt.DOCUMENT_TOPIC )
		
		self.logger.info( 'Extracting term-topic matrix...' )
		self.extractTermTopicMatrix()
		
		self.logger.info( 'Extracting document-topic matrix...' )
		self.extractDocumentTopicMatrix()
		
		self.logger.info( 'Writing data to disk...' )
		self.model.write()
	
	def readAsList( self, model_path, filename ):
		data = []
		filename = '{}/{}'.format( model_path, filename )
		with open( filename, 'r' ) as f:
			data = f.read().decode( 'utf-8' ).splitlines()
		return data
	
	# Need for STMT, which generates a mixed-string-float document-topic-distributions.csv file
	def readCsvAsMatrixStr( self, model_path, filename ):
		"""
		Return a matrix (list of list) of string values.
		Each row corresponds to a line of the input file.
		Each cell (in a row) corresponds to a comma-separated value (in each line).
		"""
		data = []
		filename = '{}/{}'.format( model_path, filename )
		with open( filename, 'r' ) as f:
			lines = UnicodeReader( f, delimiter = ',' )
			data = [ d for d in lines ]
		return data
	
	def extractDocumentTopicMatrix( self ):
		"""
		Extract document-topic matrix.
		Probability distributions are stored from the 2nd column onward in the document-topic distributions.
		"""
		matrix = []
		for line in self.document_topic_counts:
			matrix.append( map( float, line[1:self.model.topic_count+1] ) )
		self.model.document_topic_matrix = matrix
	
	def extractTermTopicMatrix( self ):
		"""
		Extract term-topic matrix.
		Transpose the input topic-term distributions.
		Ensure all values are greater than or equal to 0.
		"""
		matrix = [ [0] * self.model.topic_count ] * self.model.term_count
		for j, line in enumerate( self.topic_term_counts ):
			for i, value in enumerate(line):
				matrix[i][j] = max( 0, float(value) )
		self.model.term_topic_matrix = matrix

def main():
	parser = argparse.ArgumentParser( description = 'Import results from STMT (Stanford Topic-Modeling Toolbox) into Termite.' )
	parser.add_argument( 'config_file'          , type = str, default = None        , help = 'Path of Termite configuration file.' )
	parser.add_argument( '--topic-model-library', type = str, dest = 'model_library', help = 'Override topic model format'         )
	parser.add_argument( '--topic-model-path'   , type = str, dest = 'model_path'   , help = 'Override topic model path'           )
	parser.add_argument( '--data-path'          , type = str, dest = 'data_path'    , help = 'Override data path'                  )
	parser.add_argument( '--logging'            , type = int, dest = 'logging'      , help = 'Override logging level'              )
	args = parser.parse_args()
	
	model_library = None
	model_path = None
	data_path = None
	logging_level = 20
	
	# Read in default values from the configuration file
	config = ConfigParser.RawConfigParser()
	config.read( args.config_file )
	model_library = config.get( 'TopicModel', 'library' )
	model_path = config.get( 'TopicModel', 'path' )
	data_path = config.get( 'Termite', 'path' )
	if config.has_section( 'Misc' ):
		if config.has_option( 'Misc', 'logging' ):
			logging_level = config.getint( 'Misc', 'logging' )
	
	# Read in user-specifiec values from the program arguments
	if args.model_library is not None:
		model_library = args.model_library
	if args.model_path is not None:
		model_path = args.model_path
	if args.data_path is not None:
		data_path = args.data_path
	if args.logging is not None:
		logging_level = args.logging
	
	ImportStmt( logging_level ).execute( model_library, model_path, data_path )

if __name__ == '__main__':
	main()
