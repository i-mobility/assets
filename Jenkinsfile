import groovy.json.JsonOutput

node {
    cleanWs()

    def isDevelopment = (env.BRANCH_NAME == "master") ? false : true

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
                
                # delete old translations
                rm "\$TRANSLATIONS_FOLDER/\$LOCALE_DE_FILENAME"
                rm "\$TRANSLATIONS_FOLDER/\$LOCALE_EN_FILENAME"

                DE_LOCALE_RESPONSE=\$(
                    curl \
                        --request GET \
                        --fail \
                        --header "Authorization: token ${PHRASEAPPTOKEN}" \
                        --output "\$TRANSLATIONS_FOLDER/\$LOCALE_DE_FILENAME" \
                        "https://\$PHRASEAPP_API/projects/\$PROJECT_ID/locales/\$LOCALE_DE/download?file_format=\$FILE_FORMAT"
                )

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

            if (isDevelopment) {
                echo "only master branch pushes proper GITHUB releases, every else creates pre-releases"
            }

            sh """
                API_URL="api.github.com"
                UPLOAD_API_URL="uploads.github.com"
                OWNER="i-mobility"
                REPO="assets"
                VERSION=${newTag}
                RELEASE_JSON_RESPONSE_FOLDER="release-json-responses"

                mkdir -p "\$RELEASE_JSON_RESPONSE_FOLDER"

                API_CREATION_JSON=\$(
                    printf '{
                        "tag_name": "%s",
                        "target_commitish": "development",
                        "name": "v%s",
                        "body": "Release of version %s",
                        "draft": false,
                        "prerelease": ${isDevelopment}
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

                    echo \$RELEASE_RESPONSE > "\$RELEASE_JSON_RESPONSE_FOLDER/\$(basename \$resolution_zip .zip).json"
                done
            """
        }
    }

    stage('send github asset release urls to slack') {
        def assetsNameUrlMap = [:]

        if (isDevelopment) {
            assetsNameUrlMap['testdpi'] = 'https://download.example.com/testdpi.zip'

            def slackMessageMap = [
                testAssets:assetsNameUrlMap
            ]

            def slackMessageJson = JsonOutput.toJson(slackMessageMap)
            slackMessageJson = JsonOutput.prettyPrint(slackMessageJson)
            slackSend(channel: '@UD4FPD79T', message: '```' + slackMessageJson + '```')
        }

        sh """
            tmp_asset_name_url_file="tmp_asset_name_url_file"
            asset_json_file="assets.json"
            # ESCAPE SHELL $ FOR JENKINS GROOVY SYNTAX
            for response_json in "release-responses"/*
            do
                release_resolution_zip_name=\$(cat "\$response_json" | grep 'name' | cut -d '"' -f 4 )
                release_resolution_name=\$(basename "\$release_resolution_zip_name" .zip)
                release_url=\$(cat "\$response_json" | grep 'browser_download_url' | cut -d '"' -f 4 )

                printf "%s %s\n" "\$release_resolution_name" "\$release_url" >> "\$tmp_asset_name_url_file"
            done

            #create final json file
            cat tmp_asset_name_url_file | jq -sR '{"assets": [split("\n")[:-1][] | split(" ") | {(.[0]): .[1]}] | add }' > \$asset_json_file
        """

        def asset_json_file_content = sh(
            script: "cat assets.json",
            returnStdout: true
        ).trim()

        slackMessageJson = JsonOutput.prettyPrint(asset_json_file_content)
        slackSend(channel: '@UD4FPD79T', message: '```' + slackMessageJson + '```')
    }
}