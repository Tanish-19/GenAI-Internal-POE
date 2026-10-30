pipeline {
    agent any

    environment {
        PATH       = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        IMAGE_NAME = 'medical-image-app'
        IMAGE_TAG  = "${BUILD_NUMBER}"
        TEST_PORT  = '8502'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Verify Project Files') {
            steps {
                echo 'Verifying necessary files exist...'
                sh '''
                    test -f Dockerfile || { echo "Dockerfile missing"; exit 1; }
                    test -f medical.py || { echo "medical.py missing"; exit 1; }
                    test -f requirements.txt || { echo "requirements.txt missing"; exit 1; }
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG} and ${IMAGE_NAME}:latest"
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Smoke Test & Health Check') {
            steps {
                echo "Starting test container on port ${TEST_PORT} to run health checks..."
                sh """
                    # Clean up any previously existing test container
                    docker rm -f test-${IMAGE_NAME} 2>/dev/null || true

                    # Start test container
                    docker run -d --name test-${IMAGE_NAME} -p ${TEST_PORT}:8501 ${IMAGE_NAME}:${IMAGE_TAG}

                    # Allow container a few seconds to boot up Streamlit
                    sleep 6

                    # Verify Streamlit health endpoint
                    curl --fail --retry 3 --retry-delay 2 http://localhost:${TEST_PORT}/_stcore/health || curl -I http://localhost:${TEST_PORT}/
                """
            }
        }
    }

    post {
        always {
            echo 'Cleaning up test container...'
            sh """
                docker rm -f test-${IMAGE_NAME} 2>/dev/null || true
            """
        }
        success {
            echo "✅ Pipeline successfully built and validated ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "❌ Pipeline failed! Please check the logs above."
        }
    }
}
