def base = load 'jenkins/Jenkinsfile.base.groovy'
base.pipelineTemplate(
  branch: env.BRANCH_NAME,
  imageName: "amor573/tojuresto",
  deployTarget: "k8s" 
)
