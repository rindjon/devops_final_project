# Deploy MySQL and Flask App on Minikube

## Step 1: Prepare the Minikube Environment
1. **Start Minikube with the specified configurations**:
   ```bash
   minikube start --driver=docker --cni=cilium --kubernetes-version=stable --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=AlwaysAllow --extra-config=kubelet.cgroup-driver=systemd --extra-config=kubelet.read-only-port=10255 --insecure-registry="registry.k8s.io" --nodes 3
   ```

2. **Enable Minikube Docker (for building images)**:
   ```bash
   eval $(minikube docker-env)
   ```

---

## Step 2: Build and Deploy the Application
1. **Build the Docker Image**:
   ```bash
   docker build -t ornahum72/flask-mysql-app:latest .
   ```

2. **Push the Docker Image (optional)**:
   ```bash
   docker login
   docker push ornahum72/flask-mysql-app:latest
   ```

---

## Step 3: Prepare Persistent Storage
1. **Create the Local Storage Directory on the Node**:
   ```bash
   minikube ssh --node=minikube-m03
   sudo mkdir -p /mnt/disks/local-storage
   sudo chmod 777 /mnt/disks/local-storage
   exit
   ```

2. **Apply the Storage Resources**:
   - StorageClass:
     ```bash
     kubectl apply -f storageclass.yaml
     ```
   - PersistentVolume:
     ```bash
     kubectl apply -f PersistentVolumes.yaml
     ```
   - PersistentVolumeClaim:
     ```bash
     kubectl apply -f PersistentVolumeClaim.yaml
     ```

3. **Verify Storage**:
   ```bash
   kubectl get pv
   kubectl get pvc
   ```

---

## Step 4: Deploy MySQL
1. **Deploy MySQL StatefulSet**:
   ```bash
   kubectl apply -f StatefulSet.yaml
   ```

2. **Deploy MySQL Service**:
   ```bash
   kubectl apply -f service_mysql.yaml
   ```

3. **Verify Pod Status**:
   ```bash
   kubectl get pods
   ```

4. **If the Pod is Stuck**:
   - Check pod events:
     ```bash
     kubectl describe pod mysql-0
     ```
   - Fix issues (e.g., missing directory or permissions).

---

## Step 5: Deploy the Flask App
1. **Apply the Flask Deployment**:
   ```bash
   kubectl apply -f flask-app-deployment.yaml
   ```

2. **Apply the Flask Service**:
   ```bash
   kubectl apply -f service.yaml
   ```

3. **Access the Flask App**:
   - Get the service URL:
     ```bash
     minikube service flask-app
     ```

---

## Step 6: Verify MySQL Database and Table
1. **Access the MySQL Pod**:
   ```bash
   kubectl exec -it mysql-0 -- bash
   ```

2. **Log In to MySQL**:
   ```bash
   mysql -u root -p
   ```
   Use the root password (`password`).

3. **Switch to the Database**:
   ```sql
   USE logs_db;
   ```

4. **Check the Table**:
   ```sql
   SHOW TABLES;
   SELECT * FROM logs;
   ```

5. **Exit MySQL**:
   ```sql
   EXIT;
   ```

6. **Exit the Pod**:
   ```bash
   exit
   ```

---

## Step 7: Troubleshooting
- **Check Pod Logs**:
   ```bash
   kubectl logs mysql-0
   ```

- **Verify PersistentVolume and PVC**:
   ```bash
   kubectl describe pv local-pv-1
   kubectl describe pvc mysql-data-mysql-0
   ```

- **Restart Pods**:
   ```bash
   kubectl delete pod mysql-0