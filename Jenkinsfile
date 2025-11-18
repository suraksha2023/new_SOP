pipeline {
    agent any

    environment {
        // Path to Python executable if not in system PATH
        PYTHON = "python3"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                // Remove everything in workspace including old .git and venv
                // deleteDir()
                echo "Skipping workspace cleanup to avoid locked files"
            }
        }

        stage('Checkout Code') {
            steps {
                git(
                    url: 'https://github.com/suraksha2023/new_SOP.git',
                    branch: 'master' // or main if your repo uses it
                    // credentialsId: ''  // Uncomment if your repo is private
                )
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create a Python virtual environment, upgrade pip, install dependencies
                sh "${env.PYTHON} -m venv venv"
                sh "./venv/bin/python -m pip install --upgrade pip"
                sh "./venv/bin/pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                // Ensure workspace is on PYTHONPATH for package imports
                sh "export PYTHONPATH=\$(pwd):\$PYTHONPATH && ./venv/bin/python -m pytest -v tests"
                // For HTML report:
                // sh "export PYTHONPATH=\$(pwd):\$PYTHONPATH && ./venv/bin/python -m pytest --html=reports/report.html --self-contained-html tests"
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }
    }

    post {
        always {
            echo "Build finished — workspace cleaned up if needed."
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
