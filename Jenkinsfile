node {
    cleanWs()

    stage("checkout") {
        checkout scm
    }

    stage('zipping resolution folders') {
        sh '''
            OUTPUT_FOLDER="output"
            for resolution_entry in "images"/*
            do
                RESOLUTION_FOLDERNAME=$(basename $resolution_entry)
                mkdir -p $OUTPUT_FOLDER
                zip -FSr $OUTPUT_FOLDER/$RESOLUTION_FOLDERNAME.zip "$resolution_entry" "definitions.json" "translations"
            done
        '''
    }

    def currentTag = sh(returnStdout: true, script: "git tag --contains | head -1").trim()
    def newTag = (currentTag?.trim()) ? 1 : currentTag + 1

    stage('tag and push tags, push zip files to github') {
        withCredentials([string(credentialsId: '1acb794c-0cc8-43cd-9580-f97347847122', variable: 'GITHUBTOKEN')]) {
            sh '''
                UPLOAD_URL="api.github.com"
                OWNER="i-mobility"
                REPO="assets"
                RELEASE_ID="$newTag"

                # create a release
                curl \
                    --header "tag_name: v$newTag" \
                    --header "draft: true " \
                    --header "Token: $GITHUBTOKEN" \
                    --request POST \
                    "https://$UPLOAD_URL/repos/$OWNER/$REPO/releases"

                # upload a release
                for resolution_zip in "output"/*
                do
                    curl \
                        --header "Content-Type: application/zip" \
                        --header "Token: $GITHUBTOKEN"
                        --request POST \
                        --data "name:resolution_zip" \
                        "https://$UPLOAD_URL/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets"
                done
            '''
        }
    }
}   
