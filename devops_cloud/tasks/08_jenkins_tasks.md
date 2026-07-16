# Practice Tasks: Module 8 - Jenkins Pipelines

This document outlines step-by-step tasks to practice writing declarative Jenkinsfiles, managing workspace caching, and configuring environment credentials.

---

## Task 1: Declarative Jenkinsfile Configuration
*   **Goal**: Create a declarative Jenkinsfile executing checkout, linting, and workspace cleanup stages.
*   **Step-by-Step Instructions**:
    1. Create a file named `Jenkinsfile` in your repository root:
       ```groovy
       // Jenkinsfile
       pipeline {
           agent any
           
           options {
               timeout(time: 30, unit: 'MINUTES')
               disableConcurrentBuilds()
               ansiColor('xterm')
           }
           
           stages {
               stage('Initialize') {
                   steps {
                       echo "Initializing build environment. Version: ${BUILD_NUMBER}"
                   }
               }
               stage('Code Checkout') {
                   steps {
                       checkout scm
                   }
               }
               stage('Mock Test execution') {
                   steps {
                       sh 'echo "Running test suite execution..."'
                       sh 'python3 -c "print(\'Tests completed successfully.\')"'
                   }
               }
           }
           
           post {
               always {
                   echo "Cleaning workspace directory."
                   cleanWs()
               }
               success {
                   echo "Build succeeded."
               }
               failure {
                   echo "Build failed. Check console output logs."
               }
           }
       }
       ```
       Write this file to disk:
       ```bash
       tee Jenkinsfile << 'EOF'
       pipeline {
           agent any
           
           options {
               timeout(time: 30, unit: 'MINUTES')
               disableConcurrentBuilds()
               ansiColor('xterm')
           }
           
           stages {
               stage('Initialize') {
                   steps {
                       echo "Initializing build environment. Version: ${BUILD_NUMBER}"
                   }
               }
               stage('Code Checkout') {
                   steps {
                       checkout scm
                   }
               }
               stage('Mock Test execution') {
                   steps {
                       sh 'echo "Running test suite execution..."'
                       sh 'python3 -c "print(\'Tests completed successfully.\')"'
                   }
               }
           }
           
           post {
               always {
                   echo "Cleaning workspace directory."
                   cleanWs()
               }
               success {
                   echo "Build succeeded."
               }
               failure {
                   echo "Build failed. Check console output logs."
               }
           }
       }
       EOF
       ```
*   **Verification**:
    Commit the `Jenkinsfile` to your repository. Create a new Pipeline job in your Jenkins console, configure the source control to target your repository, and run the build. Verify all stages run successfully.

---

## Task 2: Credentials Injection
*   **Goal**: Safely inject database credentials and secrets into your Jenkins pipeline environments.
*   **Step-by-Step Instructions**:
    1. Open your Jenkins dashboard and navigate to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials**.
    2. Add a new credential:
       *   Kind: **Username with password** or **Secret text**.
       *   ID: `database-credentials-id`.
       *   Value: Configure username/password values.
    3. Modify your `Jenkinsfile` to load the credentials using `withCredentials`:
       ```groovy
       // Add stage in Jenkinsfile
       stage('Database Operations') {
           steps {
               withCredentials([usernamePassword(credentialsId: 'database-credentials-id', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                   sh 'echo "Connecting to database as user $DB_USER..."'
                   // Do not echo DB_PASS directly
                   sh 'python3 -c "import os; print(\'Authenticated successfully.\' if os.getenv(\'DB_PASS\') else \'Fail\')"'
               }
           }
       }
       ```
*   **Verification**:
    Verify the build completes successfully and the database passwords are automatically masked (`****`) in the console logs.
