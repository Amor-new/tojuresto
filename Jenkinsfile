node {
  // 🔍 Show what's actually in the workspace
  sh 'echo WORKSPACE CONTENT && find . -type f'

  // 🔁 Then try to load the file
  def base = load 'jenkins/Jenkinsfile.base.groovy'
  base.pipelineTemplate(
    branch: env.BRANCH_NAME,
    imageName: "amor573/tojuresto",
    deployTarget: "k8s"
  )
}
