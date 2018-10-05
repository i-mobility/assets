import groovy.json.JsonOutput

node {
    cleanWs()

    def currentTag
    def newTag

    stage("checkout, tag and push new tag") {
        checkout scm

        sh 'git fetch --tags'

        currentTag = sh(
            script: "git tag | sort -n | tail -1",
            returnStdout: true
        ).trim()

        newTag = (currentTag == "") ? (1) : (currentTag.toInteger() + 1)

        if(env.BRANCH_NAME == "master") {
            sh "git tag ${newTag}"
            sh 'git push --tag'
        }
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
                
                # delete old translations
                echo "\$(ls translations)"
                rm "\$TRANSLATIONS_FOLDER/\$LOCALE_DE_FILENAME"
                rm "\$TRANSLATIONS_FOLDER/\$LOCALE_EN_FILENAME"

                echo "\$(cat translations/de.json)"

                DE_LOCALE_RESPONSE=\$(
                    curl \
                        --request GET \
                        --fail \
                        --header "Authorization: token ${PHRASEAPPTOKEN}" \
                        --output "\$TRANSLATIONS_FOLDER/\$LOCALE_DE_FILENAME" \
                        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_DE/download?file_format=\$FILE_FORMAT"
                )

                echo "content of de.json: \$(cat de.json)"
                echo "\$(ls translations)"

                EN_LOCALE_RESPONSE=\$(
                    curl \
                        --request GET \
                        --fail \
                        --header "Authorization: token ${PHRASEAPPTOKEN}" \
                        --output "\$TRANSLATIONS_FOLDER/\$LOCALE_EN_FILENAME" \
                        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_EN/download?file_format=\$FILE_FORMAT"
                )
            """
        }
    }

    stage('zipping resolution folders') {
        sh './zip-resolution-folders.sh'

        if(env.BRANCH_NAME == "development") {
            sh 'ls -al output'
        }
    }

    stage('create github release and push zip files to github as releases') {
        withCredentials([string(credentialsId: '1acb794c-0cc8-43cd-9580-f97347847122', variable: 'GITHUBTOKEN')]) {
            if(env.BRANCH_NAME == "master") {
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
                            --fail \
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
                    RELEASE-JSON-RESPONSE-FOLDER="release-json-responses"
                    mkdir -p "\$RELEASE-JSON-RESPONSE-FOLDER"

                    for resolution_zip in "output"/*
                    do
                        echo "\$(ls -al output)"
                        RELEASE_RESPONSE=\$(
                            curl \
                                --request POST \
                                --fail \
                                --header "Authorization: token \${GITHUBTOKEN}" \
                                --header "Content-Type: application/zip" \
                                --data-binary @\$resolution_zip \
                                "https://\$UPLOAD_API_URL/repos/\$OWNER/\$REPO/releases/\$RELEASE_ID/assets?name=\$(basename \$resolution_zip)"
                        )

                        echo \$RELEASE_RESPONSE > "\$RELEASE-JSON-RESPONSE-FOLDER/\$(basename \$resolution_zip .zip).json"
                    done
                """
            } else {
                echo "only master branch pushes GITHUB releases"
            }
        }
    }

    stage('send github asset release urls to slack') {
        def assetsNameUrlMap = [:]

        if(env.BRANCH_NAME == "master") {
            def releaseApiResponses = findFiles(glob: 'release-json-response/*.json')
            releaseApiResponses.each {
                def responseJson = readJson file: it
                def url = responseJson['browser-download-url']
                def name_withExtension = responseJson['name']
                def name = name_withExtension.take(name_withExtension.lastIndexOf('.'))
                assetsNameUrlMap[name] = url
            }

            def slackMessageMap = [
                assets:[
                    assetsNameUrlMap
                ]
            ]

            def slackMessageJson = JsonOutput.toJson(slackMessageMap)
            slackMessageJson = JsonOutput.prettyPrint(slackMessageJson)
            slackSend(channel: '@toni', message: slackMessageJson, tokenCredentialId: 'jenkins-slack')
        } else {
            assetsNameUrlMap['testdpi'] = 'https://download.example.com/testdpi.zip'
            def slackMessageMap = [
                testAssets:[
                    assetsNameUrlMap
                ]
            ]
            def slackMessageJson = JsonOutput.toJson(slackMessageMap)
            slackMessageJson = JsonOutput.prettyPrint(slackMessageJson)
            slackSend(channel: '@toni', message: slackMessageJson, tokenCredentialId: 'jenkins-slack')
        }
    }
}
