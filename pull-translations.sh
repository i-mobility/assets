#!/bin/bash
PHRASEAPP_API="api.phraseapp.com/api/v2"
FILE_FORMAT="simple_json"
PROJECT_ID="a486755273fdfdbf597e52ebb6239543"
TRANSLATIONS_FOLDER="translations"
LOCALE_DE="a5e2374e79b53d4768c73a1d7fd38a0f"
LOCALE_EN="9449c672d4258a1dbdac76d429a39323"
LOCALE_DE_FILENAME="de.json"
LOCALE_EN_FILENAME="en.json"
TAGS="remoteassets"

mkdir translations

DE_LOCALE_RESPONSE=\$(
    curl \
        --request GET \
        --fail \
        --header "Authorization: token ${PHRASEAPPTOKEN}" \
        --output "\$TRANSLATIONS_FOLDER/\$LOCALE_DE_FILENAME" \
        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_DE/download?convert_emoji=true&file_format=\$FILE_FORMAT&tags=\$TAGS"
)

EN_LOCALE_RESPONSE=\$(
    curl \
        --request GET \
        --fail \
        --header "Authorization: token ${PHRASEAPPTOKEN}" \
        --output "\$TRANSLATIONS_FOLDER/\$LOCALE_EN_FILENAME" \
        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_EN/download?convert_emoji=true&file_format=\$FILE_FORMAT&tags=\$TAGS"
)
