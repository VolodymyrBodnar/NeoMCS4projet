# Cheat Sheet: Deploying a FastAPI Project on AWS EC2

## **1. Setting Up AWS EC2 Instance**

### **1.1. Launch an EC2 Instance**

1. Go to **AWS Management Console** → EC2 → Launch Instance.
2. Choose **Ubuntu 22.04 LTS** as the Amazon Machine Image (AMI).
3. Select an instance type (e.g., `t2.micro` for free tier).
4. Configure security groups to allow:
    - **Port 22 (SSH)** for remote access.
    - **Port 80 (HTTP)** and **Port 443 (HTTPS)** for web traffic.
    - **Port 8000** if running FastAPI directly.
5. Download and save the **SSH key (`.pem`)**.

### **1.2. Connect to EC2 via SSH**

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

## **2. Install Required Packages**

### **2.1. Update System Packages**

```bash
sudo apt update && sudo apt upgrade -y
```

### **2.2. Install Python & Pip**

```bash
sudo apt install python3-pip python3-venv -y
```

### **2.3. Install Git & Other Dependencies**

```bash
sudo apt install git nginx -y
```

## **3. Deploy FastAPI Project**

### **3.1. Clone Your FastAPI Repository**

```bash
git clone https://github.com/your-repo.git
cd your-repo
```

### **3.2. Create and Activate Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **3.3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3.4. Run FastAPI with Uvicorn (Test Locally)**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## **4. Set Up Gunicorn & Supervisor**

### **4.1. Install Gunicorn**

```bash
pip install gunicorn
```

### **4.2. Create a Gunicorn Service**

```bash
sudo nano /etc/systemd/system/fastapi.service
```

Paste the following:

```ini
[Unit]
Description=Gunicorn instance to serve FastAPI
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/your-repo
Environment="PATH=/home/ubuntu/your-repo/venv/bin"
ExecStart=/home/ubuntu/your-repo/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Save and exit (`CTRL+X`, `Y`, `Enter`).

### **4.3. Start & Enable Service**

```bash
sudo systemctl start fastapi
sudo systemctl enable fastapi
sudo systemctl status fastapi
```

## **5. Configure Nginx as a Reverse Proxy**

### **5.1. Create Nginx Configuration**

```bash
sudo nano /etc/nginx/sites-available/fastapi
```

Paste the following:

```nginx
server {
    listen 80;
    server_name your-ec2-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Save and exit.

### **5.2. Enable Configuration**

```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
sudo nginx -t  # Check for errors
sudo systemctl restart nginx
```

## **6. Configure Firewall (Optional)**

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## **7. Enable HTTPS with Let's Encrypt (Optional but Recommended)**

### **7.1. Install Certbot**

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### **7.2. Obtain SSL Certificate**

```bash
sudo certbot --nginx -d your-domain.com
```

### **7.3. Auto-Renew SSL**

```bash
sudo certbot renew --dry-run
```

## **8. Automatic Deployment (Optional)**

### **8.1. Setup Git Hooks for Deployment**

On your local machine, add a remote server:

```bash
git remote add ec2 ubuntu@your-ec2-ip:/home/ubuntu/your-repo
```

Push changes and pull on EC2:

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip 'cd /home/ubuntu/your-repo && git pull && sudo systemctl restart fastapi'
```

## **9. Monitoring & Logs**

### **9.1. View Service Logs**

```bash
sudo journalctl -u fastapi --no-pager --lines=50
```

### **9.2. View Nginx Logs**

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## **10. Summary & Next Steps**

- **For database support**, install PostgreSQL or MySQL.
- **For scaling**, consider Load Balancer or Kubernetes.
- **For auto-deployment**, use GitHub Actions or AWS CodeDeploy.
- **For security**, restrict SSH access and monitor logs.