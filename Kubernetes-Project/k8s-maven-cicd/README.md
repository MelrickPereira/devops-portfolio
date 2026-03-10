# DevOps CI/CD Pipeline – Maven, Nexus, Docker, Kubernetes

## Project Overview

This project demonstrates a **complete DevOps pipeline** where a Java application is:

1. Built using Maven
2. Stored in a Nexus artifact repository
3. Containerized using Docker
4. Pushed to Docker Hub
5. Deployed to Kubernetes using Minikube

The project helps understand how modern DevOps systems automate **build, packaging, and deployment workflows**.

---

# Architecture Diagram

```
                  ┌───────────────┐
                  │   Developer   │
                  │   (GitHub)    │
                  └───────┬───────┘
                          │
                          ▼
                ┌──────────────────┐
                │   Maven Build    │
                │  (Compile + JAR) │
                └────────┬─────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │   Nexus Repository    │
             │  Artifact Management  │
             └────────┬──────────────┘
                      │
                      ▼
              ┌───────────────────┐
              │   Docker Build    │
              │   Containerize    │
              └────────┬──────────┘
                       │
                       ▼
              ┌───────────────────┐
              │    Docker Hub     │
              │   Image Registry  │
              └────────┬──────────┘
                       │
                       ▼
             ┌─────────────────────┐
             │      Kubernetes     │
             │     Deployment      │
             │   (Minikube Cluster)│
             └─────────────────────┘
```

---

# Technologies Used

| Tool             | Purpose                  |
| ---------------- | ------------------------ |
| Apache Maven     | Build automation tool    |
| Nexus Repository | Artifact repository      |
| Docker           | Containerization         |
| Docker Hub       | Container registry       |
| Kubernetes       | Container orchestration  |
| Minikube         | Local Kubernetes cluster |
| GitHub           | Source code management   |

---

# Project Structure

```
k8s-demo
│
├── src
│   └── main/java/com/devops/App.java
│
├── pom.xml
│
├── Dockerfile
│
├── k8s
│   └── deployment.yaml
│
└── README.md
```

---

# Step 1 – Build Java Application

Build the project using Maven:

```
mvn clean package
```

This generates the artifact:

```
target/k8s-demo-1.0.jar
```

---

# Step 2 – Run Nexus Repository

Run Nexus using Docker:

```
docker run -d -p 8081:8081 --name nexus sonatype/nexus3
```

Open Nexus in browser:

```
http://localhost:8081
```

Login credentials:

```
username: admin
password: docker exec nexus cat /nexus-data/admin.password
```

Create a repository:

```
maven-releases
```

Deploy artifact to Nexus:

```
mvn deploy
```

---

# Step 3 – Build Docker Image

Create a `Dockerfile`:

```
FROM eclipse-temurin:17

WORKDIR /app

COPY target/k8s-demo-1.0.jar app.jar

CMD ["java","-jar","app.jar"]
```

Build Docker image:

```
docker build -t k8s-demo .
```

Verify image:

```
docker images
```

---

# Step 4 – Push Image to Docker Hub

Login to Docker:

```
docker login
```

Tag image:

```
docker tag k8s-demo <dockerhub-username>/k8s-demo:1.0
```

Push image:

```
docker push <dockerhub-username>/k8s-demo:1.0
```

---

# Step 5 – Start Kubernetes Cluster

Start Minikube:

```
minikube start
```

Check cluster:

```
kubectl get nodes
```

---

# Step 6 – Deploy Application to Kubernetes

Create `deployment.yaml`:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-demo

spec:
  replicas: 2

  selector:
    matchLabels:
      app: k8s-demo

  template:
    metadata:
      labels:
        app: k8s-demo

    spec:
      containers:
      - name: k8s-demo
        image: <dockerhub-username>/k8s-demo:1.0
```

Deploy application:

```
kubectl apply -f k8s/deployment.yaml
```

Check pods:

```
kubectl get pods
```

---

# Kubernetes Debug Commands

View pods:

```
kubectl get pods
```

Describe pod:

```
kubectl describe pod <pod-name>
```

View logs:

```
kubectl logs <pod-name>
```

Restart deployment:

```
kubectl rollout restart deployment k8s-demo
```

Delete pods:

```
kubectl delete pods --all
```

---

# DevOps Pipeline Summary

The complete workflow implemented in this project:

```
Source Code
    ↓
Maven Build
    ↓
Nexus Artifact Repository
    ↓
Docker Image Build
    ↓
Docker Hub Registry
    ↓
Kubernetes Deployment
```

---

# Learning Outcomes

This project demonstrates:

* Maven build lifecycle
* Artifact management using Nexus
* Docker container creation
* Container registry usage
* Kubernetes deployment
* DevOps pipeline workflow

---

# Future Improvements

Possible enhancements:

* Add Kubernetes Service (NodePort / LoadBalancer)
* Implement CI/CD using GitHub Actions
* Use Helm charts for deployment
* Add monitoring using Prometheus & Grafana
* Add logging using ELK stack
