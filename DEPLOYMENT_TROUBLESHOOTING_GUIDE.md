# Django cPanel Deployment Troubleshooting Guide
## Complete Solutions Reference

This document contains all challenges faced and solutions implemented during the deployment of Django application to Razorhost cPanel on September 22, 2025.

---

## 🔴 Challenge 1: Missing Python Dependencies
**Error:** `ModuleNotFoundError: No module named 'dj_database_url'`

**Symptoms:**
- Django commands failing with import errors
- Application not starting due to missing modules

**Root Cause:**
- Requirements not properly installed in virtual environment
- Missing critical packages: dj-database-url, python-decouple, mysqlclient

**Solution:**
1. Updated `requirements.txt` and `requirements_production.txt` with all dependencies:
   ```
   asgiref==3.9.1
   dj-database-url==3.0.1
   Django==5.2.5
   gunicorn==23.0.0
   mysqlclient==2.2.1
   packaging==25.0
   pillow==11.3.0
   python-decouple==3.8
   sqlparse==0.5.3
   whitenoise==6.11.0
   ```

2. Install via cPanel Python App:
   ```python
   import subprocess
   packages = ['dj-database-url', 'python-decouple', 'whitenoise', 'mysqlclient']
   for package in packages:
       subprocess.run(['pip', 'install', package])
   ```

---

## 🔴 Challenge 2: Git Repository Lost During Deployment
**Error:** `fatal: not a git repository (or any of the parent directories): .git`

**Symptoms:**
- Cannot pull updates from GitHub
- Git Version Control showing error code 128

**Root Cause:**
- `.cpanel.yml` deployment script removed `.git` directory
- cPanel deployment process overwrote Git configuration

**Solution:**
1. Created `.cpanel.yml` file with proper deployment configuration:
   ```yaml
   ---
   deployment:
     tasks:
       - export DEPLOYPATH=/home/meenvstf/public_html/sumithrakp/
       - /bin/cp -R * $DEPLOYPATH
       - /bin/chmod 755 $DEPLOYPATH
       - /bin/touch $DEPLOYPATH/passenger_wsgi.py
   ```

2. Recreated Git repository connection in cPanel Git Version Control

---

## 🔴 Challenge 3: MySQL Database Access Denied
**Error:** `(1044, "Access denied for user 'meenvstf_skpuser'@'localhost' to database 'meenvstf_sumithrakp'")`

**Symptoms:**
- Django unable to connect to database
- Migrations failing

**Root Cause:**
- Database user not properly added to database with privileges
- .env file missing or incorrect database credentials

**Solution:**
1. In cPanel MySQL Databases:
   - Created database: `meenvstf_sumithrakp`
   - Created user: `meenvstf_skpuser`
   - Added user to database with ALL PRIVILEGES

2. Created `.env` file in `/home/meenvstf/public_html/sumithrakp/`:
   ```
   SECRET_KEY=*+ku^im30-g_2ald84j3p6v*p%(=j*!122_@hei$igjj=r_-yy
   DEBUG=False
   ALLOWED_HOSTS=sumithrakp.com,www.sumithrakp.com
   DATABASE_URL=mysql://meenvstf_skpuser:password@localhost:3306/meenvstf_sumithrakp
   ```

---

## 🔴 Challenge 4: 404 Error on Main Domain
**Error:** Main website showing 404 error

**Symptoms:**
- `https://sumithrakp.com/` returning 404
- Admin panel redirecting to `/sumithrakp.com/admin`

**Root Cause:**
- cPanel Python App forcing Application URL to be `sumithrakp.com` instead of empty
- Document root pointing to `/public_html` instead of `/public_html/sumithrakp`
- Passenger BaseURI incorrectly set

**Solution Attempts & Issues:**
1. **Attempted:** Change Application URL to empty
   - **Issue:** cPanel forced it as dropdown with only `sumithrakp.com` option
   
2. **Attempted:** Change domain document root
   - **Issue:** cPanel didn't allow editing main domain document root

3. **Final Solution:** Fixed `.htaccess` Passenger configuration:
   ```apache
   PassengerAppRoot "/home/meenvstf/public_html/sumithrakp"
   PassengerBaseURI "/"
   PassengerPython "/home/meenvstf/virtualenv/public_html/sumithrakp/3.11/bin/python"
   ```

---

## 🔴 Challenge 5: 500 Internal Server Error
**Error:** Website showing 500 error after fixing routing

**Symptoms:**
- Application recognized but crashing
- Error logs showing recursion depth exceeded

**Root Cause:**
- `passenger_wsgi.py` file corrupted by cPanel with recursive import:
   ```python
   # WRONG - caused infinite recursion
   import imp
   wsgi = imp.load_source('wsgi', 'passenger_wsgi.py')
   application = wsgi.application
   ```

**Solution:**
Replaced `passenger_wsgi.py` with correct content:
```python
#!/usr/bin/env python
import os
import sys

project_home = '/home/meenvstf/public_html/sumithrakp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumithrakp_website.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🔴 Challenge 6: Superuser Creation Failed
**Error:** `Superuser creation skipped due to not running in a TTY`

**Symptoms:**
- Cannot create superuser via Python App Execute Script
- Interactive commands not working in cPanel

**Root Cause:**
- cPanel Python execution environment doesn't support interactive input
- TTY not available for password prompts

**Solution:**
Created non-interactive superuser creation script:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumithrakp_website.settings')
os.chdir('/home/meenvstf/public_html/sumithrakp')
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sumithrakp.com', 'password')
```

---

## 🔴 Challenge 7: Content Not Appearing (Empty Database)
**Error:** Website structure loads but no content displays

**Symptoms:**
- Pages loading but empty
- No projects, services, or testimonials showing
- Admin panel empty

**Root Cause:**
- All development data in local SQLite database
- Production MySQL database empty after migrations
- Data not transferred between databases

**Solution:**
1. Export data from SQLite:
   ```bash
   python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > data.json
   ```

2. Push to GitHub and pull on server

3. Import to MySQL:
   ```python
   import subprocess
   os.chdir('/home/meenvstf/public_html/sumithrakp')
   subprocess.run(['python', 'manage.py', 'loaddata', 'data.json'])
   ```

---

## 🔴 Challenge 8: Static Files Not Loading
**Error:** CSS, JavaScript, and images not loading

**Symptoms:**
- Page appears unstyled
- Images showing as broken links
- JavaScript functionality not working

**Root Cause:**
- Static files not collected to `staticfiles` directory
- URL routing not configured for static files
- WhiteNoise not properly configured

**Solution:**
1. Collected static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. Updated `.htaccess` for static file serving:
   ```apache
   RewriteCond %{REQUEST_URI} ^/static/
   RewriteRule ^static/(.*)$ /sumithrakp/staticfiles/$1 [L]
   ```

3. Configured WhiteNoise in settings.py:
   ```python
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

---

## 🔴 Challenge 9: Python Version Compatibility
**Issue:** Using Python 3.11.13 in cPanel

**Potential Problems:**
- mysqlclient version compatibility
- Deprecated modules (imp module warning)

**Solution:**
- Downgraded mysqlclient from 2.2.4 to 2.2.1 for better compatibility
- Removed deprecated imp module usage in passenger_wsgi.py
- Verified all packages compatible with Python 3.11

---

## 🔴 Challenge 10: Environment Variables Configuration
**Issue:** Sensitive data exposed in settings.py

**Symptoms:**
- SECRET_KEY visible in code
- Database credentials in repository

**Solution:**
1. Implemented python-decouple for environment variables
2. Created `.env` file (not in Git)
3. Updated settings.py:
   ```python
   from decouple import config, Csv
   SECRET_KEY = config('SECRET_KEY')
   DEBUG = config('DEBUG', default=False, cast=bool)
   ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
   ```

---

## 🔴 Challenge 11: cPanel Terminal Access
**Issue:** No Terminal access in cPanel

**Symptoms:**
- Cannot run commands directly
- SSH not configured

**Workarounds Used:**
1. Python App "Execute Python Script" feature:
   ```python
   import subprocess
   result = subprocess.run(['command', 'args'], capture_output=True, text=True)
   ```

2. Created Python scripts for common tasks:
   - `create_superuser.py`
   - `deploy.sh`

3. Used Git for file transfers instead of direct editing

---

## 🔴 Challenge 12: Admin URL Routing Issue
**Error:** `/admin/` redirecting to `/sumithrakp.com/admin/`

**Symptoms:**
- Double URL path in redirects
- Admin panel inaccessible

**Root Cause:**
- Passenger BaseURI configuration conflict
- Application URL forcing subdirectory behavior

**Solution:**
- Ensured PassengerBaseURI set to "/" in .htaccess
- Removed URL rewrite rules that were duplicating paths

---

## 📋 Final Working Configuration

### .htaccess (in /public_html/)
```apache
PassengerAppRoot "/home/meenvstf/public_html/sumithrakp"
PassengerBaseURI "/"
PassengerPython "/home/meenvstf/virtualenv/public_html/sumithrakp/3.11/bin/python"
```

### Python App Settings
- Python version: 3.11
- Application root: `public_html/sumithrakp`
- Application URL: (forced to `sumithrakp.com` by cPanel)
- Startup file: `passenger_wsgi.py`
- Entry point: `application`

### Database
- Type: MySQL
- Database: `meenvstf_sumithrakp`
- User: `meenvstf_skpuser`
- Connection via DATABASE_URL in .env

### File Structure
```
/public_html/
├── .htaccess
├── sumithrakp/
│   ├── passenger_wsgi.py
│   ├── manage.py
│   ├── .env
│   ├── requirements.txt
│   ├── staticfiles/
│   ├── media/
│   └── sumithrakp_website/
│       └── settings.py
```

---

## 🚀 Deployment Checklist for Future

1. **Local Preparation:**
   - [ ] Update requirements.txt
   - [ ] Test with DEBUG=False locally
   - [ ] Export data: `python manage.py dumpdata > data.json`
   - [ ] Commit and push to GitHub

2. **cPanel Setup:**
   - [ ] Create MySQL database and user
   - [ ] Set up Python App
   - [ ] Configure Git Version Control
   - [ ] Create .env file with production settings

3. **Deployment:**
   - [ ] Pull from GitHub
   - [ ] Install requirements
   - [ ] Run migrations
   - [ ] Load data
   - [ ] Collect static files
   - [ ] Create superuser
   - [ ] Restart Python app

4. **Verification:**
   - [ ] Test main website
   - [ ] Test admin panel
   - [ ] Test static files loading
   - [ ] Check error logs

---

## 🛠 Useful Commands & Scripts

### Check Django Configuration
```python
import subprocess
result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True)
print(result.stdout)
```

### View Error Logs
```python
with open('/home/meenvstf/logs/sumithrakp.com/error.log', 'r') as f:
    print(f.read()[-1000:])  # Last 1000 characters
```

### Restart Application
```python
import subprocess
subprocess.run(['touch', 'passenger_wsgi.py'])
```

### Database Migration Status
```python
import subprocess
result = subprocess.run(['python', 'manage.py', 'showmigrations'], capture_output=True, text=True)
print(result.stdout)
```

---

## 📝 Key Learnings

1. **cPanel Python Apps have specific constraints** - Application URL dropdown may be locked
2. **Always check error logs first** - They provide exact error details
3. **Database data doesn't migrate automatically** - Must export/import manually
4. **passenger_wsgi.py is critical** - Wrong configuration causes 500 errors
5. **Git integration can break** - .cpanel.yml needs careful configuration
6. **Static files need explicit configuration** - Won't serve automatically
7. **Environment variables are essential** - Never commit sensitive data
8. **TTY not available in cPanel** - Use non-interactive scripts
9. **File permissions matter** - 755 for directories, 644 for files
10. **Test deployment check:** `python manage.py check --deploy`

---

## 🔗 Important File Locations

- Error Logs: `/home/meenvstf/logs/`
- Python App Config: `/home/meenvstf/.cpanel/`
- Virtual Environment: `/home/meenvstf/virtualenv/public_html/sumithrakp/3.11/`
- Application Files: `/home/meenvstf/public_html/sumithrakp/`
- Static Files: `/home/meenvstf/public_html/sumithrakp/staticfiles/`

---

## 📞 When to Contact Hosting Support

Contact Razorhost support when:
- Terminal/SSH access needed but not available
- Python App URL dropdown locked to specific value
- Domain document root cannot be changed
- Passenger configuration being overwritten
- Git Version Control not available
- SSL certificate installation needed

---

*Document created: September 22, 2025*
*Deployment completed successfully with all issues resolved*