# Kubernetes Pod Deployment with Minikube

This project demonstrates how to deploy a containerized application
using **Kubernetes Pods** on a **local Kubernetes cluster created with
Minikube**, using **Docker as the container runtime**.

------------------------------------------------------------------------

## 🚀 Technologies Used

-   Docker Desktop -- Container runtime
-   Kubernetes -- Container orchestration platform
-   Minikube -- Local Kubernetes cluster
-   kubectl -- Kubernetes command line tool

------------------------------------------------------------------------

## 📁 Project Structure

    kubernetes-pod-project
    │
    ├── pod.yaml        # Kubernetes Pod configuration
    └── README.md       # Project documentation

------------------------------------------------------------------------

## ⚙️ Prerequisites

Install the following tools before running the project:

-   Docker Desktop
-   Minikube
-   kubectl

Verify installations:

``` bash
docker --version
minikube version
kubectl version --client
```

------------------------------------------------------------------------

## 🖥️ Step 1 -- Start Kubernetes Cluster

Start Minikube using Docker as the driver:

``` bash
minikube start --driver=docker
```

Check cluster status:

``` bash
minikube status
```

Verify the node:

``` bash
kubectl get nodes
```

Expected output:

    NAME       STATUS   ROLES           AGE
    minikube   Ready    control-plane

------------------------------------------------------------------------

## 📦 Step 2 -- Create Pod Configuration

Create a file called:

    pod.yaml

Add the following configuration:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx-container
    image: nginx
    ports:
    - containerPort: 80
```

------------------------------------------------------------------------

## 🚀 Step 3 -- Deploy the Pod

Navigate to the project folder:

``` bash
cd kubernetes-pod-project
```

Apply the configuration:

``` bash
kubectl apply -f pod.yaml
```

Verify pod creation:

``` bash
kubectl get pods
```

Example output:

    NAME        READY   STATUS    AGE
    nginx-pod   1/1     Running   10s

------------------------------------------------------------------------

## 🔍 Step 4 -- Inspect the Pod

Describe pod details:

``` bash
kubectl describe pod nginx-pod
```

Check container logs:

``` bash
kubectl logs nginx-pod
```

------------------------------------------------------------------------

## 🌐 Step 5 -- Access the Application

Forward the pod port to your local machine:

``` bash
kubectl port-forward pod/nginx-pod 8080:80
```

Open your browser and go to:

    http://localhost:8080

You should see the **Nginx Welcome Page**.

------------------------------------------------------------------------

## 🛑 Step 6 -- Stop the Application

Stop port forwarding:

    CTRL + C

Delete the pod:

``` bash
kubectl delete pod nginx-pod
```

------------------------------------------------------------------------

## 🧹 Step 7 -- Stop the Kubernetes Cluster

Stop Minikube:

``` bash
minikube stop
```

Delete the cluster completely:

``` bash
minikube delete
```

------------------------------------------------------------------------

## 🛠️ Useful Commands

Check pods:

``` bash
kubectl get pods
```

Check nodes:

``` bash
kubectl get nodes
```

View logs:

``` bash
kubectl logs nginx-pod
```

Check pod details:

``` bash
kubectl describe pod nginx-pod
```

------------------------------------------------------------------------

## 📚 Key Concepts Demonstrated

-   Kubernetes Pods
-   Container orchestration
-   YAML configuration
-   kubectl CLI usage
-   Local Kubernetes clusters using Minikube

------------------------------------------------------------------------

## 📸 Screenshots

Add screenshots of:

1.  `kubectl get pods`
2.  `minikube status`
3.  Nginx running in browser
4.  Pod deployment command

------------------------------------------------------------------------

## 📌  Description:

Deployed a containerized application using Kubernetes Pods on a local
Minikube cluster, managed using kubectl and Docker.
