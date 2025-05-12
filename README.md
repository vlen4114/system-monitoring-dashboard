# System Monitoring Dashboard

A real-time system monitoring dashboard built with **Flask** and **Plotly** that displays CPU, memory, disk, and network metrics with a modern UI.
![image](https://github.com/user-attachments/assets/16c7a281-8d87-40a6-8680-e73cd8f51358)


---

## 🔧 Features

- ✅ Real-time system metrics monitoring
- 📊 Interactive gauges and charts
- 🔍 Process monitoring
- 💻 System information display
- 🚨 Alert system for critical conditions
- 📱 Responsive design
- 🐳 Docker container support
- ☸️ Kubernetes deployment ready

---

## 📦 Prerequisites

- Python 3.7+
- pip
- Docker (for containerization)
- AWS CLI (for ECR/EKS deployment)
- `kubectl` (for Kubernetes deployment)

---

## 🚀 Installation

### ✅ Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vlen4114/system-monitoring-dashboard.git
   cd system-monitoring-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 app.py
   ```

4. Access the dashboard at: [http://localhost:5000](http://localhost:5000)

---

### 🐳 Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t system-monitor .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 system-monitor
   ```

3. Access the dashboard at: [http://localhost:5000](http://localhost:5000)

---

### ☁️ AWS ECR/EKS Deployment

#### 1. Push to Amazon ECR

- **Create an ECR repository**:
   ```python
   import boto3

   ecr_client = boto3.client('ecr')
   repository_name = 'system-monitor-repo'
   response = ecr_client.create_repository(repositoryName=repository_name)
   repository_uri = response['repository']['repositoryUri']
   print(repository_uri)
   ```

- **Authenticate Docker to ECR**:
   ```bash
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
   ```

- **Tag and push your image**:
   ```bash
   docker tag system-monitor:latest <repository-uri>:latest
   docker push <repository-uri>:latest
   ```

#### 2. Deploy to Amazon EKS

- **Create an EKS cluster and node group** via AWS Console or CLI

- **Create deployment and service** (save as `eks.py`):
   ```python
   from kubernetes import client, config

   config.load_kube_config()
   api_client = client.ApiClient()

   deployment = client.V1Deployment(
       metadata=client.V1ObjectMeta(name="system-monitor"),
       spec=client.V1DeploymentSpec(
           replicas=1,
           selector=client.V1LabelSelector(
               match_labels={"app": "system-monitor"}
           ),
           template=client.V1PodTemplateSpec(
               metadata=client.V1ObjectMeta(labels={"app": "system-monitor"}),
               spec=client.V1PodSpec(
                   containers=[client.V1Container(
                       name="system-monitor-container",
                       image="<your-ecr-repo-uri>:latest",
                       ports=[client.V1ContainerPort(container_port=5000)]
                   )]
               )
           )
       )
   )

   api_instance = client.AppsV1Api(api_client)
   api_instance.create_namespaced_deployment(namespace="default", body=deployment)

   service = client.V1Service(
       metadata=client.V1ObjectMeta(name="system-monitor-service"),
       spec=client.V1ServiceSpec(
           selector={"app": "system-monitor"},
           ports=[client.V1ServicePort(port=5000)]
       )
   )

   api_instance = client.CoreV1Api(api_client)
   api_instance.create_namespaced_service(namespace="default", body=service)
   ```

- **Run the deployment**:
   ```bash
   python3 eks.py
   ```

- **Verify deployment**:
   ```bash
   kubectl get deployment -n default
   kubectl get service -n default
   kubectl get pods -n default
   ```

- **Access the service**:
   ```bash
   kubectl port-forward service/system-monitor-service 5000:5000
   ```

   Then visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
system-monitoring-dashboard/
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Dashboard HTML template
├── Dockerfile            # Docker configuration
└── eks.py                # Kubernetes deployment script
```

---

## ⚙️ Customization

- **Update refresh rate**: Modify `REFRESH_INTERVAL` in `templates/index.html`
- **Change alert thresholds**: Update thresholds in `app.py`
- **Customize UI**: Edit CSS section in `index.html`

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📬 Contact

For questions, feedback, or suggestions, feel free to open an issue or reach out directly.
