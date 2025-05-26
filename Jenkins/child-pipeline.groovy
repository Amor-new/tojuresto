pipeline {
    agent any

    environment {
        DOCKER_REPO = 'amor573/tojuresto'  // Your Docker Hub repo
    }

    stages {
        stage('Load Context') {
            steps {
                script {
                    def contextFile = "/var/lib/jenkins/workspace/parent-pipeline-job/context_env"
                    if (!fileExists(contextFile)) {
                        error "context_env not found: $contextFile"
                    }

                    def lines = readFile(contextFile).split("\n")
                    lines.each { line ->
                        def (key, value) = line.tokenize("=")
                        env."${key}" = value
                    }

                    env["PROJECT_NAME"] = env["GIT_URL"].tokenize("/")[4].replace(".git", "")
                    env["BRANCH_NAME"] = env["GIT_BRANCH"].tokenize("/")[1]
                }
            }
        }

        stage('Checkout') {
            steps {
                git url: "${env.GIT_URL}",
                    branch: "${env.BRANCH_NAME}",
                    credentialsId: 'github-credentials'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                  docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                  docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                      docker push ${DOCKER_REPO}:latest
                    """
                }
            }
        }

        
    }
}
