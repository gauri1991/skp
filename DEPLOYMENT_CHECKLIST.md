# Deployment Checklist for Razorhost cPanel

## ✅ Completed Fixes

- [x] Generated secure SECRET_KEY
- [x] Configured environment variables (.env file)
- [x] Updated settings.py for production compatibility
- [x] Added WhiteNoise for static file serving
- [x] Installed production dependencies (gunicorn, whitenoise)
- [x] Created passenger_wsgi.py for cPanel
- [x] Added .gitignore file
- [x] Created static files collection script

## 📋 Deployment Steps

### Before Upload:

1. [ ] Update .env file with production values:
   ```
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=mysql://cpanel_user:password@localhost:3306/cpanel_dbname
   ```

2. [ ] Create database backup (if updating existing site)

### In cPanel:

3. [ ] Create MySQL database and user
4. [ ] Upload files (exclude: venv/, db.sqlite3, .env.example)
5. [ ] Create Python application in cPanel
6. [ ] Set Python version to 3.9+
7. [ ] Set application entry point to: passenger_wsgi.py
8. [ ] Install dependencies: `pip install -r requirements.txt`

### After Upload:

9. [ ] Run migrations: `python manage.py migrate`
10. [ ] Create superuser: `python manage.py createsuperuser`
11. [ ] Collect static files: `python manage.py collectstatic`
12. [ ] Set file permissions (media folder: 755)
13. [ ] Install SSL certificate
14. [ ] Update .env for SSL:
    ```
    SECURE_SSL_REDIRECT=True
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    SECURE_HSTS_SECONDS=31536000
    ```
15. [ ] Test all functionality
16. [ ] Monitor error logs

## 🔒 Security Verification

Run after deployment:
```bash
python manage.py check --deploy
```

Expected output with SSL: All security checks should pass
Expected output without SSL: Only SSL-related warnings

## 📁 Files to Upload

- All Python files (*.py)
- templates/ directory
- static/ directory  
- main/ app directory
- requirements.txt
- passenger_wsgi.py
- .env (create new with production values)

## ❌ Do NOT Upload

- venv/ directory
- db.sqlite3
- .env.example
- __pycache__/ directories
- *.pyc files
- .git/ directory
- staticfiles/ (will be generated on server)

================================================================

 ✅ Production Ready Status: FIXED

  Your Django app is now production-ready with the following improvements:

  Fixed Issues:

  1. Secure SECRET_KEY - Generated and stored in .env
  2. Environment configuration - Using python-decouple for all sensitive settings
  3. DEBUG mode - Set to False in .env
  4. ALLOWED_HOSTS - Configured for production domains
  5. Security headers - Added (activate when SSL is configured)
  6. Static files - WhiteNoise configured for production serving
  7. Database - Configurable via DATABASE_URL

  Created Files:

  - .env - Environment variables (keep secret!)
  - passenger_wsgi.py - cPanel entry point
  - .gitignore - Prevents sensitive files from git
  - requirements.txt - Updated with all dependencies
  - DEPLOYMENT_CHECKLIST.md - Step-by-step deployment guide

  Next Steps for Razorhost cPanel:

  1. Create MySQL database in cPanel
  2. Update .env with production values
  3. Upload files (excluding venv/, db.sqlite3)
  4. Set up Python app in cPanel
  5. Run migrations and collect static files
  6. Configure SSL certificate

  The app is now ready for deployment! Follow the DEPLOYMENT_CHECKLIST.md for detailed instructions.
