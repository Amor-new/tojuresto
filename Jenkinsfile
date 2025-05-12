node {
  // ✅ Ensure code is pulled
  checkout scm

  // 🧪 Show contents of the workspace
  sh 'echo WORKSPACE CONTENT && find . -type f'

  // ✅ Now load the shared pipeline
  def base = load 'jenkins/Jenkinsfile.base.groovy'
  base.pipelineTemplate(
    branch: env.BRANCH_NAME,
    imageName: "amor573/tojuresto",
    deployTarget: "k8s"
  )
}
