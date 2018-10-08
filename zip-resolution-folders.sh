#!/bin/sh

# script to zip assets with individual resolutions separately and puts all of them in an output folder
# requirements: needed folders/files: images/<resolution>, translations, definitions.json
# result: each zip holds a folder with assets, the definsions.json and the translations folders

OUTPUT_FOLDER="output"

mkdir -p $OUTPUT_FOLDER

# create a master zip including all of the content
zip -r $OUTPUT_FOLDER/"master".zip "images" "translations" "definitions.json"

# create a zip for each resolution
cp -R translations "$OUTPUT_FOLDER/translations"
cp -R definitions.json "$OUTPUT_FOLDER/definitions.json"

for resolution_entry in "images"/*
do
    RESOLUTION_FOLDERNAME=$(basename $resolution_entry)
    mkdir "$OUTPUT_FOLDER/images"

    cp -R "$resolution_entry/." "$OUTPUT_FOLDER/images/"
    cp -R translations "$OUTPUT_FOLDER/translations"
    cp -R definitions.json "$OUTPUT_FOLDER/definitions.json"

    cd "$OUTPUT_FOLDER"
    zip -r $RESOLUTION_FOLDERNAME.zip "images" "translations" "definitions.json"

    rm -Rf "images"
    rm -Rf "translations"
    rm -f "definitions.json"
    cd ..
done

rm -Rf "$OUTPUT_FOLDER/translations"
rm -f "$OUTPUT_FOLDER/definitions.json"
