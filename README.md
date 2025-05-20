DevOps CI/CD Pipeline Project
This repository contains a fully automated CI/CD pipeline setup for a containerized application using Jenkins, Docker, and Kubernetes (Minikube). It includes security scanning with Snyk, multi-environment deployment support (Docker Compose & Kubernetes), and pipeline modularization with Jenkins Shared Libraries.

📦 Features
Automated Builds on push to main/qa/dev branches

Snyk Security Scanning of application dependencies and container images

Multi-Environment Deployments:

dev branch: deploys using Docker Compose

qa branch: deploys using Docker Compose

main branch: deploys to Kubernetes (Minikube) via remote VM

Modular Jenkins Pipeline using Shared Library (vars/tojurestoPipeline.groovy)

Dockerized Jenkins Master with all necessary dependencies (Docker CLI, kubectl, Snyk CLI)

🛠️ Technologies Used
Jenkins (Dockerized)

Docker & Docker Compose

Kubernetes (Minikube inside VM)

Snyk for image and dependency scanning

GitHub Webhooks for automated pipeline triggers

SSH-based remote deployment

📁 Project Structure
arduino
Copy
Edit
.
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile (entry point)
├── requirements.txt
├── entrypoint.sh
├── k8s/
│ ├── deployment.yaml
│ └── service.yaml
├── vars/
│ └── tojurestoPipeline.groovy
└── README.md
⚙️ Deployment Logic
Branch Action
dev Pull image to VM and deploy via Docker Compose
qa Pull image to VM and deploy via Docker Compose
main SSH into VM and deploy to Kubernetes using kubectl and Kubeconfig

🔐 Security
All Docker images are scanned via Snyk at build time

CI pipeline enforces fast feedback with --insecure-skip-tls-verify only in test pipelines

Secrets are managed through Jenkins Credentials Plugin

🚀 Running Locally
To run this project:

Clone the repository

Build and run Jenkins:

bash
Copy
Edit
docker-compose up --build
Access Jenkins at http://localhost:8080

Add required credentials (Docker Hub, Snyk token, SSH keys)

Trigger builds via GitHub Webhook (via Ngrok or reverse proxy)
