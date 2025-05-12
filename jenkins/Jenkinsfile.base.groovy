def pipelineTemplate(Map config = [:]) {
  pipeline {
    agent any

    environment {
      IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
      stage('Checkout') {
        steps {
          checkout scm
        }
      }

      stage('Docker Login & Build') {
        steps {
          withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh """
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker build -t ${config.imageName}:${IMAGE_TAG} .
              docker tag ${config.imageName}:${IMAGE_TAG} ${config.imageName}:latest
            """
          }
        }
      }

      stage('Authenticate Snyk') {
        steps {
          withCredentials([string(credentialsId: 'synk-token', variable: 'SNYK_TOKEN')]) {
            sh 'snyk auth $SNYK_TOKEN'
          }
        }
      }

      stage('Snyk Image Scan') {
        steps {
          sh "snyk container test ${config.imageName}:${IMAGE_TAG}"
        }
      }

      stage('Push Image to Docker Hub') {
        steps {
          withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh """
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker push ${config.imageName}:${IMAGE_TAG}
              docker push ${config.imageName}:latest
            """
          }
        }
      }

      stage('Deploy') {
        steps {
          script {
            if (config.deployTarget == 'docker-compose') {
              sshagent(['vm-ssh-cred-id']) {
                sh """
                  ssh -o StrictHostKeyChecking=no amor@192.168.176.135 '
                    docker pull ${config.imageName}:${IMAGE_TAG} &&
                    docker stop landing-container || true &&
                    docker rm landing-container || true &&
                    docker run -d --name landing-container -p 80:80 ${config.imageName}:${IMAGE_TAG}
                  '
                """
              }
            } else if (config.deployTarget == 'k8s') {
              sh """
                kubectl set image deployment/tojuresto tojuresto=${config.imageName}:${IMAGE_TAG}
                kubectl rollout status deployment/tojuresto
              """
            }
          }
        }
      }
    }
  }
}

return this
// This is a shared library function that can be used in Jenkins pipelines.
// It defines a pipeline template that builds a Docker image, scans it with Snyk, and deploys it to either Docker Compose or Kubernetes.
// The pipeline consists of several stages: