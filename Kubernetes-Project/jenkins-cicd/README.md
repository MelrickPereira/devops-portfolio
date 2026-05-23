# 🚀 Jenkins CI/CD Pipeline with Docker and Kubernetes

## 📌 Project Overview

This project demonstrates a **complete DevOps CI/CD pipeline** using **Jenkins, Docker, and Kubernetes**.
The pipeline automatically builds, containerizes, and deploys an application whenever code is pushed to the repository.

This project simulates a real-world DevOps workflow where code moves from development to deployment automatically.

---

# 🏗️ Architecture

```
Developer → GitHub → Jenkins Pipeline → Docker → Kubernetes (Minikube)
```

1. Developer pushes code to GitHub
2. Jenkins pipeline triggers
3. Jenkins builds the application
4. Docker image is created
5. Image is pushed to DockerHub
6. Application is deployed to Kubernetes

---

# 🛠️ Technologies Used

* Jenkins
* Git & GitHub
* Maven
* Docker
* DockerHub
* Kubernetes
* Minikube
* Linux (Ubuntu)

---

# 📂 Project Structure

```
jenkins-ci-cd-project
│
├── src/
│
├── pom.xml
│
├── Dockerfile
│
├── Jenkinsfile
│
└── k8s-deployment.yaml
```

---

# ⚙️ Jenkins Setup

### 1️⃣ Install Jenkins

Install Jenkins on Ubuntu and start the service.

```
sudo apt update
sudo apt install jenkins
sudo systemctl start jenkins
```

Open Jenkins:

```
http://localhost:8080
```

---

### 2️⃣ Unlock Jenkins

Retrieve the initial admin password:

```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Paste it into the Jenkins UI.

---

### 3️⃣ Install Suggested Plugins

Click **Install Suggested Plugins** during setup.

Important plugins installed:

* Git Plugin
* Pipeline Plugin
* Docker Pipeline Plugin
* Maven Integration Plugin

---

### 4️⃣ Create Admin User

Create your Jenkins admin account.

Example:

```
Username: admin
Password: ********
Full Name: Melrick Pereira
Email: your-email
```

---

# ⚙️ Configure Jenkins Tools

Go to:

```
Manage Jenkins → Global Tool Configuration
```

Add the following tools:

### Git

```
Name: Git
```

### Maven

```
Name: Maven3
Install Automatically: Enabled
```

---

# 🐳 Dockerfile

This Dockerfile packages the application into a container.

```
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY target/*.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]
```

---

# ☸️ Kubernetes Deployment

`k8s-deployment.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: java-app
  template:
    metadata:
      labels:
        app: java-app
    spec:
      containers:
      - name: java-app
        image: dockerhub-username/java-app:latest
        ports:
        - containerPort: 8080
```

---

# 🔄 Jenkins Pipeline

`Jenkinsfile`

```
pipeline {
    agent any

    tools {
        maven 'Maven3'
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/yourusername/jenkins-ci-cd-project.git'
            }
        }

        stage('Build Application') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t dockerhub-username/java-app .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push dockerhub-username/java-app'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s-deployment.yaml'
            }
        }

    }
}
```

---

# ▶️ Running the Pipeline

Start Minikube:

```
minikube start
```

Verify Kubernetes cluster:

```
kubectl get nodes
```

Run the Jenkins pipeline:

```
Build Now
```

---

# 🔍 Verify Deployment

Check pods:

```
kubectl get pods
```

Check services:

```
kubectl get svc
```

---

# 📈 CI/CD Pipeline Stages

| Stage        | Description                        |
| ------------ | ---------------------------------- |
| Clone        | Jenkins pulls code from GitHub     |
| Build        | Maven compiles the project         |
| Docker Build | Docker image is created            |
| Docker Push  | Image pushed to DockerHub          |
| Deploy       | Application deployed to Kubernetes |

---



---

# 👨‍💻 Author

**Melrick Pereira**
Computer Engineer
