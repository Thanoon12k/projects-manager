# Deployment Guide

## Production Deployment Checklist

### 1. Environment Setup

- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set strong `SECRET_KEY`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up static file serving
- [ ] Configure media file storage (cloud storage recommended)
- [ ] Set up SSL/HTTPS certificate
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure caching (Redis recommended)

### 2. Database Setup

#### PostgreSQL (Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE projectmanager;
CREATE USER projectuser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE projectmanager TO projectuser;
\q
```

Update `.env`:
```env
DB_NAME=projectmanager
DB_USER=projectuser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 3. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Use WhiteNoise or CDN for serving
```

### 4. Media Files

For production, use cloud storage:

#### AWS S3 Example
```python
# Install boto3
pip install boto3 django-storages

# Update settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
```

### 5. Web Server Configuration

#### Gunicorn + Nginx

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Create Gunicorn service** (`/etc/systemd/system/gunicorn.service`)
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project_manager
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/project_manager/gunicorn.sock project_manager.wsgi:application

[Install]
WantedBy=multi-user.target
```

3. **Nginx Configuration** (`/etc/nginx/sites-available/project_manager`)
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/project_manager/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/project_manager/media/;
    }
    
    location / {
        proxy_pass http://unix:/path/to/project_manager/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **Enable and start services**
```bash
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl enable nginx
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 7. Environment Variables

Create `.env` file with production values:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=projectmanager
DB_USER=projectuser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=/path/to/credentials.json
GOOGLE_SHEETS_SPREADSHEET_NAME=ProjectManager

# Twilio
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis (if using)
REDIS_URL=redis://127.0.0.1:6379/1
```

### 8. Security Checklist

- [ ] Change default admin URL
- [ ] Use strong passwords
- [ ] Enable two-factor authentication
- [ ] Set up firewall rules
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up monitoring (Sentry, etc.)

### 9. Backup Strategy

```bash
# Database backup script
#!/bin/bash
pg_dump -U projectuser projectmanager > backup_$(date +%Y%m%d_%H%M%S).sql

# Media files backup
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### 10. Monitoring

Set up monitoring tools:
- **Application Monitoring**: Sentry, Rollbar
- **Server Monitoring**: New Relic, Datadog
- **Uptime Monitoring**: UptimeRobot, Pingdom
- **Log Aggregation**: ELK Stack, Papertrail

### 11. Deployment Platforms

#### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Railway
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

#### DigitalOcean App Platform
1. Connect repository
2. Configure build and run commands
3. Set environment variables
4. Deploy

### 12. Post-Deployment

- [ ] Test all functionality
- [ ] Verify SSL certificate
- [ ] Test API endpoints
- [ ] Check static files serving
- [ ] Verify media uploads
- [ ] Test Google Sheets sync
- [ ] Test WhatsApp messaging
- [ ] Set up automated backups
- [ ] Configure monitoring alerts

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `collectstatic`
   - Check STATIC_ROOT path
   - Verify Nginx configuration

2. **Database connection errors**
   - Check database credentials
   - Verify PostgreSQL is running
   - Check firewall rules

3. **Media files not accessible**
   - Check file permissions
   - Verify MEDIA_ROOT path
   - Check Nginx configuration

4. **500 Internal Server Error**
   - Check logs: `tail -f logs/django.log`
   - Verify DEBUG=False doesn't hide errors
   - Check ALLOWED_HOSTS

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and rotate secrets quarterly
- Backup database daily
- Monitor logs weekly
- Security audit quarterly
- Performance optimization as needed

