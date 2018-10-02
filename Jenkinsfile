node {
    cleanWs()

    def currentTag
    def newTag

    stage("checkout, tag and push new tag") {
        checkout scm

        currentTag = sh(
            script: "git name-rev --tags --name-only \$(git rev-parse HEAD)",
            returnStdout: true
        ).trim()

        echo "currentTag: ${currentTag}"

        sh 'git name-rev --tags --name-only \$(git rev-parse HEAD)'
        newTag = (currentTag == "undefined") ? 1 : currentTag + 1

        echo "newTag: ${newTag}"

        sh 'git tag \$newTag'
        sh 'git push --tag'
    }

    stage('zipping resolution folders') {
        sh './zip-resolution-folders.sh'
    }

    stage('create github release and push zip files to github as releases') {
        withCredentials([string(credentialsId: '1acb794c-0cc8-43cd-9580-f97347847122', variable: 'GITHUBTOKEN')]) {
            sh '''
                UPLOAD_URL="api.github.com"
                OWNER="i-mobility"
                REPO="assets"
                VERSION=1

                API_CREATION_JSON=$(
                    printf '{
                        "tag_name": "%s",
                        "target_commitish": "master",
                        "name": "v%s",
                        "body": "Release of version %s",
                        "draft": false,
                        "prerelease": false
                    }' $VERSION $VERSION $VERSION
                )

                # create a release
                curl \
                    --request POST \
                    --header "Authorization: token ${GITHUBTOKEN}" \
                    --data "$API_CREATION_JSON" \
                    "https://$UPLOAD_URL/repos/$OWNER/$REPO/releases"

                # upload a release
                for resolution_zip in "output"/*
                do
                    curl \
                        --header "Content-Type: application/zip" \
                        --header "Authorization: token ${GITHUBTOKEN}" \
                        --request POST \
                        --data "name: $resolution_zip" \
                        "https://$UPLOAD_URL/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets"
                done
            '''
        }
    }
}
