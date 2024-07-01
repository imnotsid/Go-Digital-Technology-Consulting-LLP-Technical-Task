pipeline {
    agent any  // Use any available agent

    environment {
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
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
                        docker.image("${DOCKER_IMAGE}:latest").push('latest')
                    }
                }
            }
        }

        stage('Deploy with Terraform') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        sh 'terraform init'
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }
    }

    post {
        always {
            // Ensure archiveArtifacts is used inside a node context
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            junit '**/target/test-*.xml'
        }
    }
}
