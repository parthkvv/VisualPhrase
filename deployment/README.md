# Setup for Deployment

## API's to enable in GCP for Project
* Compute Engine API
* Service Usage API
* Cloud Resource Manager API
* Google Container Registry API
* Kubernetes Engine API

## Create a Service Account for Deployment
- Roles required:
    - Compute Admin
    - Compute OS Login
    - Container Registry Service Agent
    - Kubernetes Engine Admin
    - Service Account User
    - Storage Admin
- Create and download a private key. Copy this file into a `secrets` folder within the `deployment` directory and rename it to `deployment.json`.

## Start Deployment Docker Container
-  `cd deployment`
- Run `sh docker-shell.sh`

## SSH Setup
Configuring OS Login for service account
```
gcloud compute project-info add-metadata --project autocap-gcp --metadata enable-oslogin=TRUE
```

Create an SSH Key for Service Account
```
cd /secrets
ssh-keygen -f ssh-key-deployment
cd /app
```

Providing Public SSH Keys to Instances
```
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub
```
From the output of the above command keep note of the username. Add this username to the `ansible_user` field within `scripts/inventory.yml`.

# Deployment

Start deployment Docker container as described above.

## Build and Push Docker Containers to GCR (Google Container Registry)
```
ansible-playbook deploy-docker-images.yml -i inventory.yml
```

## Create and Deploy Kubernetes Cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
```

## Delete cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=absent
```