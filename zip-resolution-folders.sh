#!/bin/sh

# script to zip assets with individual resolutions separately and puts all of them in an output folder
# requirements: needed folders/files: images/<resolution>, translations, definitions.json
# result: each zip holds a folder with assets, the definsions.json and the translations folders

OUTPUT_FOLDER="output"

mkdir -p $OUTPUT_FOLDER
echo "$(ls)"

for resolution_entry in "images"/*
do
    RESOLUTION_FOLDERNAME=$(basename $resolution_entry)
    mkdir "$OUTPUT_FOLDER/images"

    cp -R "$resolution_entry/." "$OUTPUT_FOLDER/images/"

    cd "$OUTPUT_FOLDER"
    zip -r $RESOLUTION_FOLDERNAME.zip "images" "../translations" "../definitions.json"
    # cd ..
    # zip -ur $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "translations" "definitions.json"
    ## zip -u $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "definitions.json"

    # rm -Rf "$OUTPUT_FOLDER/images"
    rm -Rf "images"
done
