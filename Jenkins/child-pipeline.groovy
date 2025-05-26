pipeline {
    agent any

    environment {
        DOCKER_REPO = 'amor573/tojuresto'
    }

    stages {
        stage('Load Context') {
            steps {
                script {
                    context = [:]
                    def contextFile = "/var/jenkins_home/workspace/parent-pipeline-job/context_env"
                    if (!fileExists(contextFile)) {
                        error "context_env not found: $contextFile"
                    }

                    def lines = readFile(contextFile).split("\n")
                    lines.each { line ->
                        def (key, value) = line.tokenize("=")
                        context[key.trim()] = value.trim()
                    }

                    echo "Loaded context: GIT_URL=${context['GIT_URL']}, GIT_BRANCH=${context['GIT_BRANCH']}"
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    git url: "${context['GIT_URL']}",
                        branch: "${context['GIT_BRANCH'].split('/')[1]}",
                        credentialsId: 'github-credentials'
                }
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
