# Deployment Guide for Razorhost cPanel

## Production Readiness Assessment

### ✅ FIXED Issues:
1. **DEBUG** - Now configurable via environment variable (set to False)
2. **SECRET_KEY** - Generated secure key, stored in .env
3. **ALLOWED_HOSTS** - Configured for production domains
4. **Security settings** - Added (will activate when SSL is enabled)
5. **Database** - Configurable via DATABASE_URL
6. **Environment variables** - Implemented using python-decouple

### ⚠️ Remaining Considerations:
- SSL/HTTPS needs to be configured on the server
- MySQL database needs to be set up in cPanel
- Media files directory needs proper permissions

## Steps to Deploy on Razorhost cPanel

### 1. Prepare Your Application

1. **Create MySQL Database in cPanel:**
   - Go to MySQL Databases
   - Create new database (e.g., `sumithra_db`)
   - Create database user with strong password
   - Add user to database with ALL privileges

2. **Set up Environment Variables:**
   - Create `.env` file from `.env.example`
   - Fill in your production values:
     ```
     SECRET_KEY=generate-a-new-50-character-key
     DEBUG=False
     ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
     DB_NAME=your_cpanel_username_sumithra_db
     DB_USER=your_cpanel_username_dbuser
     DB_PASSWORD=your_secure_password
     ```

### 2. Upload Files via cPanel

1. **Compress your project:**
   ```bash
   zip -r sumithrakp_website.zip . -x "*.pyc" -x "__pycache__/*" -x "venv/*" -x ".git/*" -x "db.sqlite3"
   ```

2. **Upload to cPanel:**
   - Use File Manager or FTP
   - Upload to your domain's root directory
   - Extract the zip file

### 3. Set up Python App in cPanel

1. **Create Python Application:**
   - Go to "Setup Python App" in cPanel
   - Click "Create Application"
   - Choose Python version 3.9+ 
   - Set application root: `/home/username/yourdomain.com`
   - Set application URL: yourdomain.com
   - Set startup file: `passenger_wsgi.py`

2. **Install Dependencies:**
   - Enter virtual environment from cPanel terminal
   - Run: `pip install -r requirements_production.txt`

3. **Configure Database:**
   ```bash
   python manage.py migrate --settings=sumithrakp_website.settings_production
   python manage.py createsuperuser --settings=sumithrakp_website.settings_production
   python manage.py collectstatic --settings=sumithrakp_website.settings_production
   ```

### 4. Additional cPanel Configuration

1. **Set Environment Variables:**
   - In Python App settings, add environment variables from `.env`

2. **Configure Static Files:**
   - Create symlink or configure Apache/LiteSpeed to serve `/static/` and `/media/`

3. **SSL Certificate:**
   - Install SSL certificate (Let's Encrypt free SSL available in cPanel)
   - Force HTTPS redirect

### 5. Important Security Steps

1. **Generate new SECRET_KEY:**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Set proper file permissions:**
   ```bash
   chmod 755 -R /home/username/yourdomain.com/
   chmod 600 .env
   ```

3. **Configure Firewall:**
   - Only allow necessary ports (80, 443)

## Testing Deployment

1. Check application loads: `https://yourdomain.com`
2. Test admin panel: `https://yourdomain.com/admin`
3. Verify static files load correctly
4. Test all forms and functionality
5. Monitor error logs in cPanel

## Maintenance Commands

```bash
# Restart application
touch passenger_wsgi.py

# View logs
tail -f /home/username/logs/yourdomain.com/error.log

# Update code
git pull origin main
python manage.py migrate --settings=sumithrakp_website.settings_production
python manage.py collectstatic --settings=sumithrakp_website.settings_production
touch passenger_wsgi.py
```

## Troubleshooting

- **500 Error:** Check error logs and ensure all dependencies installed
- **Static files not loading:** Verify STATIC_ROOT and web server configuration
- **Database errors:** Check database credentials and migrations
- **Import errors:** Ensure Python version matches development environment