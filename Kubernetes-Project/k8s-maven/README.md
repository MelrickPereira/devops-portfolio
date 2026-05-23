# DevOps CI/CD Pipeline – Maven, Nexus, Docker, Kubernetes

## Project Overview

This project demonstrates an **end-to-end DevOps pipeline** for building, packaging, and deploying a Java application using modern DevOps tools.

The workflow shows how application code moves through multiple stages of a typical DevOps lifecycle:

1. **Build** – Application compiled and packaged with Maven
2. **Artifact Management** – JAR artifact stored in Nexus repository
3. **Containerization** – Application packaged as a Docker container
4. **Registry** – Docker image pushed to Docker Hub
5. **Deployment** – Container deployed to Kubernetes cluster (Minikube)

This project helps understand how real DevOps systems automate **build, artifact storage, containerization, and deployment processes**.

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

| Tool             | Purpose                                       |
| ---------------- | --------------------------------------------- |
| Apache Maven     | Build automation and dependency management    |
| Nexus Repository | Artifact repository for storing build outputs |
| Docker           | Containerization of the application           |
| Docker Hub       | Container image registry                      |
| Kubernetes       | Container orchestration platform              |
| Minikube         | Local Kubernetes cluster                      |
| GitHub           | Source code repository                        |

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

# Step 1 – Build the Java Application

Build the project using Maven:

```
mvn clean package
```

This command compiles the code and generates a packaged artifact:

```
target/k8s-demo-1.0.jar
```

---

# Maven `pom.xml` Configuration

The **`pom.xml` (Project Object Model)** is the core configuration file used by Maven.

It defines:

* Project metadata
* Dependencies
* Build plugins
* Packaging configuration
* Artifact deployment configuration

### Example Structure

```
<project xmlns="http://maven.apache.org/POM/4.0.0">

  <modelVersion>4.0.0</modelVersion>

  <groupId>com.devops</groupId>
  <artifactId>k8s-demo</artifactId>
  <version>1.0</version>

</project>
```

### Key Elements

| Element                  | Description                           |
| ------------------------ | ------------------------------------- |
| `groupId`                | Organization or project namespace     |
| `artifactId`             | Name of the application               |
| `version`                | Application version                   |
| `dependencies`           | Libraries required by the application |
| `build`                  | Build configuration                   |
| `plugins`                | Plugins used during build             |
| `distributionManagement` | Repository for artifact deployment    |

---

# Step 2 – Run Nexus Repository

Start Nexus using Docker:

```
docker run -d -p 8081:8081 --name nexus sonatype/nexus3
```

Open Nexus in browser:

```
http://localhost:8081
```

Retrieve admin password:

```
docker exec nexus cat /nexus-data/admin.password
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

Verify the image:

```
docker images
```

---

# Step 4 – Push Image to Docker Hub

Login to Docker Hub:

```
docker login
```

Tag the image:

```
docker tag k8s-demo <dockerhub-username>/k8s-demo:1.0
```

Push the image:

```
docker push <dockerhub-username>/k8s-demo:1.0
```

---

# Step 5 – Start Kubernetes Cluster

Start Minikube:

```
minikube start
```

Verify cluster:

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

Deploy the application:

```
kubectl apply -f k8s/deployment.yaml
```

Verify running pods:

```
kubectl get pods
```

---

# Kubernetes Debug Commands

Check running pods:

```
kubectl get pods
```

Describe pod:

```
kubectl describe pod <pod-name>
```

View container logs:

```
kubectl logs <pod-name>
```

Restart deployment:

```
kubectl rollout restart deployment k8s-demo
```

---

# DevOps Pipeline Summary

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
* Artifact management with Nexus
* Docker container creation
* Container registry usage
* Kubernetes deployment concepts
* DevOps CI/CD pipeline architecture

---

# Future Improvements

Potential enhancements:

* Add Kubernetes Service (NodePort / LoadBalancer)
* Implement CI/CD using GitHub Actions or Jenkins
* Use Helm charts for Kubernetes deployments
* Add monitoring with Prometheus & Grafana
* Implement centralized logging using ELK stack
