node {
    cleanWs()

    def currentTag
    def newTag

    stage("checkout, tag and push new tag") {
        checkout scm

        sh 'git fetch --tags'
        sh 'git tag | tail -1'

        currentTag = sh(
            script: "git tag | tail -1",
            returnStdout: true
        ).trim()

        newTag = (currentTag == "") ? (1) : (currentTag.toInteger() + 1)

        sh "git tag ${newTag}"
        sh 'git push --tag'
    }

    stage('pull translations from PhraseApp') {
        withCredentials([string(credentialsId: 'd1d41fbe-b0f8-4a36-b95e-960e7d6285dd', variable: 'PHRASEAPPTOKEN')]) {
            sh"""
                PHRASEAPP_API="api.phraseapp.com/api/v2/"
                FILE_FORMAT="simple_json"
                PROJECT_ID="5d1947d996b5e135178933ba3654bd38"
                TRANSLATIONS_FOLDER="translations"
                LOCALE_DE="ab544bfc73101286f93b5048d676e005"
                LOCALE_EN="165be6785e2440749b1e30818469e531"
                LOCALE_DE_FILENAME="de.json"
                LOCALE_EN_FILENAME="en.json"

                echo "\$(ls -al)"
                
                # delete old translations
                rm "\$(TRANSLATIONS_FOLDER)/\$LOCALE_DE_FILENAME"
                rm "\$(TRANSLATIONS_FOLDER)/\$LOCALE_EN_FILENAME"

                DE_LOCALE_RESPONSE=\$(
                    curl \
                        --request GET \
                        --header "Authorization: token ${PHRASEAPPTOKEN}" \
                        --output "\$(TRANSLATIONS_FOLDER)/\$LOCALE_DE_FILENAME" \
                        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_DE/download?file_format=\$FILE_FORMAT"
                )

                EN_LOCALE_RESPONSE=\$(
                    curl \
                        --request GET \
                        --header "Authorization: token ${PHRASEAPPTOKEN}" \
                        --output "\$(TRANSLATIONS_FOLDER)/\$LOCALE_EN_FILENAME" \
                        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_EN/download?file_format=\$FILE_FORMAT"
                )

                # check for failure
            """ 
        }
    }

    stage('zipping resolution folders') {
        sh './zip-resolution-folders.sh'
    }

    stage('create github release and push zip files to github as releases') {
        withCredentials([string(credentialsId: '1acb794c-0cc8-43cd-9580-f97347847122', variable: 'GITHUBTOKEN')]) {

            sh """
                API_URL="api.github.com"
                UPLOAD_API_URL="uploads.github.com"
                OWNER="i-mobility"
                REPO="assets"
                VERSION=${newTag}

                API_CREATION_JSON=\$(
                    printf '{
                        "tag_name": "%s",
                        "target_commitish": "master",
                        "name": "v%s",
                        "body": "Release of version %s",
                        "draft": false,
                        "prerelease": false
                    }' \$VERSION \$VERSION \$VERSION
                )

                # create a release
                RESPONSE=\$(
                    curl \
                        --request POST \
                        --header "Authorization: token ${GITHUBTOKEN}" \
                        --data "\$API_CREATION_JSON" \
                        "https://\$API_URL/repos/\$OWNER/\$REPO/releases"
                )

                RELEASE_ID=\$(
                    echo "\$RESPONSE" | jq '.id'
                )

                echo "github release ID: \$RELEASE_ID"

                # creating a release, results in a ID created by github

                # upload a release
                for resolution_zip in "output"/*
                do
                    echo "\$(ls -al output)"
                    curl \
                        --request POST \
                        --header "Authorization: token \${GITHUBTOKEN}" \
                        --header "Content-Type: application/zip" \
                        --data-binary @\$resolution_zip \
                        "https://\$UPLOAD_API_URL/repos/\$OWNER/\$REPO/releases/\$RELEASE_ID/assets?name=\$(basename \$resolution_zip)"
                done
            """
        }
    }
}
