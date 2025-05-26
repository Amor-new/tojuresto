pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/Amor-new/tojuresto.git'
        GIT_BRANCH = 'origin/test'
    }

    stages {
        stage("Capture Environment") {
            steps {
                sh """
                  echo "GIT_URL=${GIT_URL}" > $WORKSPACE/context_env
                  echo "GIT_BRANCH=${GIT_BRANCH}" >> $WORKSPACE/context_env
                  echo "BUILD_NUMBER=${BUILD_NUMBER}" >> $WORKSPACE/context_env
                """
            }
        }

        stage("Trigger Build Pipeline") {
            steps {
                build job: 'my-project-pipeline'
            }
        }
    }
}
