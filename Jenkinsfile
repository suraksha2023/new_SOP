pipeline {
    agent any

    environment {
        PYTHON = "python3"
        DISPLAY = ":99"  // Use Xvfb virtual display
    }

    stages {
        stage('Checkout Code') {
            steps {
                git(
                    url: 'https://github.com/suraksha2023/new_SOP.git',
                    branch: 'main'
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

        stage('Run Tests Before OTP') {
            steps {
                sh '''
                    # Start Xvfb in the background for virtual display
                    Xvfb :99 -screen 0 1920x1080x24 &
                    export DISPLAY=:99

                    mkdir -p reports
                    export PYTHONPATH=$(pwd):$PYTHONPATH

                    # Run pytest with python -m pytest to avoid file not found errors
                    ./venv/bin/python -m pytest tests/test_sop_full_ddt.py --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('OTP Input Required') {
            steps {
                script {
                    def otp = input(
                        message: 'Enter OTP to continue',
                        parameters: [string(name: 'OTP_CODE', description: 'Enter OTP here')]
                    )
                    env.OTP_VALUE = otp
                }
            }
        }

        stage('Continue After OTP') {
            steps {
                echo "OTP entered: ${env.OTP_VALUE}"
                // Add your OTP-dependent steps here
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest Report'
                ])
            }
        }
    }

    post {
        always {
            echo "Build finished"
        }
    }
}
