#!/bin/bash

# Termite Set-Up Script
#
# Run once to
#   - download necessary library files
#   - minify client javascript files
#

#LIBRARY=lib/
#STMT=stmt-0.4.0/
CLIENT_SRC=client-src/
CLIENT_LIB=client-lib/
jar_folder=libraries

# if [ ! -d $LIBRARY ]
# then
# 	echo
# 	echo "Creating a library folder: $LIBRARY"
# 	mkdir $LIBRARY
# fi

if [ ! -d $CLIENT_LIB ]
then
	echo
	echo "Creating the client template folder: $CLIENT_LIB"
	mkdir $CLIENT_LIB
fi

if [ ! -d $jar_folder ]
then
	echo
	echo "Creating the jar folder: $jar_folder"
	mkdir $jar_folder
fi

#------------------------------------------------------------------------------#
# D3 Visualization Javascript Library

# echo
# echo "Downloading D3 javascript library..."
# curl --insecure --location https://github.com/mbostock/d3/releases/download/v3.4.1/d3.v3.zip > $LIBRARY/d3.v3.zip

echo
echo "Uncompressing D3 javascript library..."
unzip $jar_folder/d3.v3.zip d3.v3.js -d $CLIENT_SRC
unzip $jar_folder/d3.v3.zip d3.v3.min.js -d $CLIENT_LIB

echo
echo "Extracting D3 license..."
unzip $jar_folder/d3.v3.zip LICENSE -d $jar_folder
mv $jar_folder/LICENSE $jar_folder/LICENSE-d3

#------------------------------------------------------------------------------#
# jQuery Javascript Library

echo
echo "Moving jQuery javascript library..."
mv $jar_folder/jquery-1.9.1.js $CLIENT_SRC/jquery.js
mv $jar_folder/jquery-1.9.1.min.js $CLIENT_LIB/jquery.min.js

# echo
# echo "Downloading jQuery GitHub archive..."
# curl --insecure --location http://github.com/jquery/jquery/archive/master.zip > $LIBRARY/jquery.zip

echo
echo "Extracting jQuery license..."
unzip $jar_folder/jquery-master.zip jquery-master/LICENSE.txt -d $jar_folder
mv $jar_folder/jquery-master/LICENSE.txt $jar_folder/LICENSE-jquery
rmdir $jar_folder/jquery-master

#------------------------------------------------------------------------------#
# Underscore Javascript Library

# echo
# echo "Downloading Underscore GitHub archive..."
# curl --insecure --location http://github.com/documentcloud/underscore/archive/master.zip > $LIBRARY/underscore-master.zip

echo
echo "Uncompressing Underscore javascript library..."
unzip $jar_folder/underscore-master.zip underscore-master/underscore.js -d $jar_folder
unzip $jar_folder/underscore-master.zip underscore-master/underscore-min.js -d $jar_folder
mv $jar_folder/underscore-master/underscore.js $CLIENT_SRC/underscore.js
mv $jar_folder/underscore-master/underscore-min.js $CLIENT_LIB/underscore.min.js

echo
echo "Extracting Underscore license..."
unzip $jar_folder/underscore-master.zip underscore-master/LICENSE -d $jar_folder
mv $jar_folder/underscore-master/LICENSE $jar_folder/LICENSE-underscore
rmdir $jar_folder/underscore-master

#------------------------------------------------------------------------------#
# Backbone Javascript Library

# echo
# echo "Downloading Backbone GitHub archive..."
# curl --insecure --location http://github.com/documentcloud/backbone/archive/master.zip > $LIBRARY/backbone-master.zip

echo
echo "Uncompressing Backbone javascript library..."
unzip $jar_folder/backbone-master.zip backbone-master/backbone.js -d $jar_folder
unzip $jar_folder/backbone-master.zip backbone-master/backbone-min.js -d $jar_folder
mv $jar_folder/backbone-master/backbone.js $CLIENT_SRC/backbone.js
mv $jar_folder/backbone-master/backbone-min.js $CLIENT_LIB/backbone.min.js

echo
echo "Extracting Backbone license..."
unzip $jar_folder/backbone-master.zip backbone-master/LICENSE -d $jar_folder
mv $jar_folder/backbone-master/LICENSE $jar_folder/LICENSE-backbone
rmdir $jar_folder/backbone-master

#------------------------------------------------------------------------------#
# Mallet (topic modeling library)

# echo
# echo "Downloading MALLET (MAchine Learning for LanguagE Toolkit)..."
# curl --insecure --location http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz > $LIBRARY/mallet-2.0.7.tar.gz

# echo
# echo "Uncompressing MALLET..."
# tar -zxvf $jar_folder/mallet-2.0.7.tar.gz mallet-2.0.7

# echo
# echo "Extracting MALLET License..."
# cp mallet-2.0.7/LICENSE $jar_folder/LICENSE-mallet

#------------------------------------------------------------------------------#
# Stanford Topic Modeling Toolkit

# echo
# echo "Downloading STMT (Stanford Topic Modeling Toolkit)..."
# if [ ! -d $STMT ]
# then
# 	echo
# 	echo "Creating a folder for STMT: $STMT"
# 	mkdir $STMT
# fi

# curl --insecure --location http://nlp.stanford.edu/software/tmt/tmt-0.4/tmt-0.4.0.jar > $STMT/tmt-0.4.0.jar
# curl --insecure --location http://nlp.stanford.edu/software/tmt/tmt-0.4/tmt-0.4.0-src.zip > $LIBRARY/tmt-0.4.0-src.zip
# mv $jar_folder/tmt-0.4.0.jar $STMT/tmt-0.4.0.jar

# echo
# echo "Extracting STMT License..."
# unzip $jar_folder/tmt-0.4.0-src.zip LICENSE -d $jar_folder
# cp $jar_folder/LICENSE $jar_folder/LICENSE-stmt

#------------------------------------------------------------------------------#
# Google closure compiler for Javascript

# echo
# echo "Downloading Google Closure Compiler..."
# curl --insecure --location http://dl.google.com/closure-compiler/compiler-latest.zip > $LIBRARY/compiler-latest.zip

echo
echo "Uncompressing Google Closure Compiler..."
unzip $jar_folder/compiler-latest.zip closure-compiler-v20180506.jar -d $jar_folder
mv $jar_folder/closure-compiler-v20180506.jar $jar_folder/closure-compiler.jar

echo
echo "Extracting Google Closure Compiler License..."
unzip $jar_folder/compiler-latest.zip COPYING -d $jar_folder
cp $jar_folder/COPYING $jar_folder/LICENSE-closure-compiler

#------------------------------------------------------------------------------#
# Slider for Firefox - Requires Java Developer Kit (JDK) - Last tested on JDK 8u231.

echo
echo "Minifying html5slider.js"
java -jar $jar_folder/closure-compiler.jar --js=$CLIENT_SRC/html5slider.js --js_output_file=$CLIENT_LIB/html5slider.min.js

#------------------------------------------------------------------------------#
# Minify javascript files - Requires Java Developer Kit (JDK) - Last tested on JDK 8u231.

echo
echo "Minifying javascript files..."

for JS_FILE in FullTermTopicProbabilityModel SeriatedTermTopicProbabilityModel FilteredTermTopicProbabilityModel TermFrequencyModel TermTopicMatrixView TermFrequencyView ViewParameters StateModel UserControlViews QueryString
do
	echo "    Minifying $JS_FILE"
	java -jar $jar_folder/closure-compiler.jar --js=$CLIENT_SRC/$JS_FILE.js --js_output_file=$CLIENT_LIB/$JS_FILE.min.js
done
