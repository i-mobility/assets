#!/bin/sh

# script to zip assets with individual resolutions separately and puts all of them in an output folder
# requirements: needed folders/files: images/<resolution>, translations, definitions.json
# result: each zip holds a folder with assets, the definsions.json and the translations folders

OUTPUT_FOLDER="output"

mkdir -p $OUTPUT_FOLDER
for resolution_entry in "images"/*
do
    RESOLUTION_FOLDERNAME=$(basename $resolution_entry)
    zip -jrm $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "$resolution_entry"
    zip -ur $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "translations"
    zip -u $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "definitions.json"
done
