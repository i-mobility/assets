import groovy.json.JsonOutput

node {
    properties([
        disableConcurrentBuilds()
   ])

    cleanWs()

    def isDevelopment = (env.BRANCH_NAME == "master") ? false : true

    def currentTag
    def newTag
    def release_json_responses_folder = "release-json-responses"

    stage("checkout, tag and push new tag") {
        checkout scm

        sh 'git fetch --tags'

        currentTag = sh(
            script: "git tag | sort -n | tail -1",
            returnStdout: true
        ).trim()

        newTag = (currentTag == "") ? (1) : (currentTag.toInteger() + 1)

        if (isDevelopment) {
          newTag = 'dev'
        }

        sh "git tag -f ${newTag}"
        sh 'git push -f --tag'
    }

    stage('pull translations from PhraseApp') {
        withCredentials([string(credentialsId: 'phrase-token', variable: 'PHRASEAPPTOKEN')]) {
            sh './pull-translations.sh'
        }
    }

    stage('zipping resolution folders') {
        sh './zip-resolution-folders.sh'

        if(env.BRANCH_NAME == "development") {
            sh 'ls -al output'
        }
    }

    stage('create github release and push zip files to github as releases') {
        withCredentials([string(credentialsId: 'prod--github-jenkins--token', variable: 'GITHUBTOKEN')]) {

            if (isDevelopment) {
                echo "only master branch pushes proper GITHUB releases, everything else creates pre-releases"
            }

            sh """#!/bin/bash
                API_URL="api.github.com"
                UPLOAD_API_URL="uploads.github.com"
                OWNER="i-mobility"
                REPO="assets"
                DEV_RELEASE_ID="13323651"
                VERSION=${newTag}

                mkdir -p "${release_json_responses_folder}"

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

                if [ "true" == "${isDevelopment}" ]; then
                  RELEASE_ID="\$DEV_RELEASE_ID"
                  for ASSET_ID in \$(curl --fail -H "Authorization: token ${GITHUBTOKEN}" -s "https://\$API_URL/repos/\$OWNER/\$REPO/releases/\$DEV_RELEASE_ID/assets" | jq .[].id)
                  do
                    curl --fail -H "Authorization: token ${GITHUBTOKEN}" -XDELETE "https://\$API_URL/repos/\$OWNER/\$REPO/releases/assets/\$ASSET_ID"
                  done
                else
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
                fi

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

                    echo \$RELEASE_RESPONSE > "${release_json_responses_folder}/\$(basename "\$resolution_zip" .zip).json"
                    echo "curl release upload response: "
                    echo "\$RELEASE_RESPONSE"
                done
            """
        }
    }

    stage('send github asset release urls to slack') {
        sh """#!/bin/bash
            tmp_asset_name_url_file="tmp_asset_name_url_file"
            asset_json_file="assets.json"
            for response_json in "${release_json_responses_folder}"/*
            do
                echo "\$response_json"
                release_resolution_zip_name=\$(cat "\$response_json" | jq .name | tr -d '"' )
                release_resolution_name=\$(basename "\$release_resolution_zip_name" .zip)
                release_url=\$(cat "\$response_json" | jq .browser_download_url | tr -d '"' )

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

        if (!isDevelopment) {
          // sends to #backend
          slackSend(
            channel: '#backend', message: '```' + slackMessageJson + '```\n\n:warning: New assets are NOT automatically used\n`v1/config`must be adapted to reference the new assets\nSee https://github.com/i-mobility/assets#releasing for more info')
        }
    }
}
