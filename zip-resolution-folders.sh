#!/bin/sh

# script to zip assets with individual resolutions separately and puts all of them in an output folder
# requirements: needed folders/files: images/<resolution>, translations, definitions.json
# result: each zip holds a folder with assets, the definsions.json and the translations folders

OUTPUT_FOLDER="output"

mkdir -p $OUTPUT_FOLDER
echo "$(ls -al)"
for resolution_entry in "images"/*
do
    echo "$(ls -al)"
    RESOLUTION_FOLDERNAME=$(basename $resolution_entry)
    zip -r $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "$resolution_entry" "definitions.json" "translations"
done
