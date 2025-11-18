pipeline {
    agent any

    environment {
        PYTHON = "python3"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                // Optional: cleanup workspace, comment if needed
                // deleteDir()
                echo "Skipping workspace cleanup to avoid locked files"
            }
        }

        stage('Checkout Code') {
            steps {
                git(
                    url: 'https://github.com/suraksha2023/new_SOP.git',
                    branch: 'main', // or 'master' depending on your repo
                    credentialsId: ''  // add if private repo
                )
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh "${env.PYTHON} -m venv venv"
                sh "./venv/bin/python -m pip install --upgrade pip setuptools wheel"
                sh "./venv/bin/pip install -r requirements.txt"
                sh "./venv/bin/pip install webdriver-manager"
            }
        }

        stage('Run Tests') {
            steps {
                sh "export PYTHONPATH=\$(pwd):\$PYTHONPATH && ./venv/bin/python -m pytest -v tests/ --html=reports/report.html --self-contained-html"
            }
        }


    stages {
        stage('Perform Step Before OTP') {
            steps {
                echo 'Running tests or steps before OTP input'
                // Your automation steps before OTP
            }
        }

        stage('Wait for OTP input') {
            steps {
                // Pause pipeline and prompt user in Jenkins UI
                input message: 'Please enter OTP to continue', parameters: [
                    string(defaultValue: '', description: 'Enter OTP here', name: 'OTP_CODE')
                ]
            }
        }

        stage('Continue After OTP') {
            steps {
                echo "Received OTP: ${params.OTP_CODE}"
                // Use OTP_CODE in your automation as needed
            }
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
            echo "Build finished"
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
