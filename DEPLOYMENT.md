# Hotel Management System - AWS Deployment Guide

## 🚀 AWS EC2 Deployment Instructions

### Prerequisites
- AWS EC2 instance running (Ubuntu/Amazon Linux)
- Docker and Docker Compose installed on EC2
- MongoDB Atlas cluster created
- SSH access to EC2 instance

### Step 1: Generate Production SECRET_KEY

On your local machine, generate a new SECRET_KEY:

```bash
python generate_secret.py
```

**⚠️ IMPORTANT:** Use a NEW secret key for production. Never reuse development keys.

### Step 2: Configure MongoDB Atlas

1. Go to MongoDB Atlas dashboard
2. Navigate to **Network Access**
3. Add your EC2 instance's public IP address to the IP whitelist
   - Or use `0.0.0.0/0` for testing (not recommended for production)
4. Get your connection string from the **Database** → **Connect** section

### Step 3: Prepare EC2 Instance

SSH into your EC2 instance:

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

Install Docker and Docker Compose if not already installed:

```bash
# For Amazon Linux 2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Log out and log back in for group changes to take effect.

### Step 4: Deploy Application

1. **Clone your repository** (or upload files):
```bash
git clone <your-repo-url>
cd Hotel-Service
```

2. **Create production `.env` file on EC2**:
```bash
nano .env
```

Add your production configuration:
```env
SECRET_KEY=<your-new-production-secret-key>
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/hotel_db
DATABASE_NAME=hotel_db
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Replace:**
- `<your-new-production-secret-key>` with the key from Step 1
- MongoDB connection string with your Atlas credentials
- CORS_ORIGINS with your actual frontend domain(s)

3. **Build and run with Docker Compose**:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

4. **Verify deployment**:
```bash
# Check if container is running
docker ps

# Check logs
docker logs hotel-api

# Test health endpoint
curl http://localhost:8000/health
```

### Step 5: Configure NGINX (Optional but Recommended)

Install NGINX:
```bash
sudo yum install -y nginx  # Amazon Linux
# or
sudo apt install -y nginx  # Ubuntu
```

Create NGINX configuration:
```bash
sudo nano /etc/nginx/conf.d/hotel-api.conf
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Start NGINX:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 6: Configure EC2 Security Group

In AWS Console:
1. Go to EC2 → Security Groups
2. Select your instance's security group
3. Add inbound rules:
   - Type: HTTP, Port: 80, Source: 0.0.0.0/0
   - Type: HTTPS, Port: 443, Source: 0.0.0.0/0 (if using SSL)
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0 (if accessing directly)

### Step 7: Test Your Deployment

```bash
# Test from EC2
curl http://localhost:8000/health

# Test from your local machine
curl http://your-ec2-public-ip/health
# or
curl http://yourdomain.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 🔄 Updating Your Application

To deploy updates:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🛡️ Security Checklist

- ✅ New SECRET_KEY generated for production
- ✅ MongoDB Atlas IP whitelist configured
- ✅ .env file NOT committed to Git
- ✅ CORS_ORIGINS set to actual frontend domains
- ✅ EC2 security groups properly configured
- ✅ Non-root user in Docker container
- ✅ HTTPS enabled (recommended - use Let's Encrypt)

## 📊 Monitoring

Check application health:
```bash
# Container status
docker ps

# Application logs
docker logs -f hotel-api

# Resource usage
docker stats
```

## 🆘 Troubleshooting

### Container won't start
```bash
docker logs hotel-api
```

### Database connection issues
- Verify MongoDB Atlas IP whitelist includes EC2 IP
- Check MONGODB_URL in .env file
- Test connection: `docker exec hotel-api python -c "from pymongo import MongoClient; client = MongoClient('your-connection-string'); print(client.server_info())"`

### Port already in use
```bash
sudo lsof -i :8000
# Kill the process if needed
```

### Reset and rebuild
```bash
docker-compose -f docker-compose.prod.yml down
docker system prune -a
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | JWT signing key | Generated 64-char hex |
| MONGODB_URL | MongoDB connection string | mongodb+srv://... |
| DATABASE_NAME | Database name | hotel_db |
| CORS_ORIGINS | Allowed frontend origins | https://example.com |

## 🔐 Important Notes

1. **Never use development SECRET_KEY in production**
2. **Always use HTTPS in production** (set up SSL/TLS with Let's Encrypt)
3. **Regularly backup your MongoDB database**
4. **Monitor your application logs**
5. **Keep Docker images updated**
6. **Use environment-specific .env files**
7. **Enable CloudWatch logs** for better monitoring (optional)

---

For issues or questions, check the application logs first:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```
