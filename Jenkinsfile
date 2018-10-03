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

        newTag = (currentTag == "undefined") ? (1) : (currentTag.toInteger() + 1)

        sh "git tag ${newTag}"
        sh 'git push --tag'
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
                        --data-binary \$resolution_zip \
                        "https://\$UPLOAD_API_URL/repos/\$OWNER/\$REPO/releases/\$RELEASE_ID/assets?name=\$(basename \$resolution_zip)"
                done
            """
        }
    }
}
