pipeline {
    agent any

    environment {
         AWS_ACCESS_KEY_ID = credentials('AKIAXUP5XUOR7AG4YGPL')
        AWS_SECRET_ACCESS_KEY = credentials('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')
        DOCKER_IMAGE = "525055009699.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo-siddhant-task"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/imnotsid/Go-Digital-Technology-Consulting-LLP-Technical-Task.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry('https://525055009699.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws-credentials') {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        stage('Deploy with Terraform') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            junit 'target/test-*.xml'
        }
    }
}
