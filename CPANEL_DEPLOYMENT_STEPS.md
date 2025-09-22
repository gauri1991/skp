# cPanel Deployment Steps for sumithrakp.com

Your Git repository is now connected to cPanel at:
- **Repository Path**: `/home/meenvstf/public_html/sumithrakp`
- **Remote URL**: `https://github.com/gauri1991/skp.git`

## Step 1: Push Code to GitHub

From your local machine:
```bash
cd /home/gss/Documents/projects/other/sumithrakp_website

# Initialize git if not already done
git init

# Add your remote
git remote add origin https://github.com/gauri1991/skp.git

# Add all files
git add .

# Commit
git commit -m "Initial deployment to cPanel"

# Push to GitHub
git push -u origin main
```

## Step 2: Pull Code in cPanel

1. Go to cPanel → Git Version Control
2. Find your repository (sumithrakp)
3. Click "Manage"
4. Click "Pull or Deploy" tab
5. Click "Update from Remote"
6. Click "Deploy HEAD Commit"

## Step 3: Set up Python App in cPanel

1. Go to "Setup Python App" in cPanel
2. Click "Create Application"
3. Configure:
   - **Python version**: 3.9 or higher
   - **Application root**: `public_html/sumithrakp`
   - **Application URL**: Leave empty for root domain
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`

4. Click "CREATE"
5. Note down the command to enter virtual environment

## Step 4: Install Dependencies

1. In cPanel Terminal or SSH:
```bash
# Enter the virtual environment (use command from Step 3)
source /home/meenvstf/virtualenv/public_html/sumithrakp/3.9/bin/activate

# Navigate to app directory
cd /home/meenvstf/public_html/sumithrakp

# Install dependencies
pip install -r requirements.txt

# Install MySQL client if using MySQL
pip install mysqlclient
```

## Step 5: Create MySQL Database

1. Go to MySQL Databases in cPanel
2. Create new database: `meenvstf_sumithrakp`
3. Create new user: `meenvstf_skpuser`
4. Add user to database with ALL privileges
5. Note the password

## Step 6: Configure Environment Variables

1. Create `.env` file in `/home/meenvstf/public_html/sumithrakp/`:
```bash
cd /home/meenvstf/public_html/sumithrakp
nano .env
```

2. Add the following (update with your actual values):
```
SECRET_KEY=*+ku^im30-g_2ald84j3p6v*p%(=j*!122_@hei$igjj=r_-yy
DEBUG=False
ALLOWED_HOSTS=sumithrakp.com,www.sumithrakp.com
DATABASE_URL=mysql://meenvstf_skpuser:YOUR_PASSWORD@localhost:3306/meenvstf_sumithrakp
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

3. Save and exit (Ctrl+X, Y, Enter)

## Step 7: Run Django Commands

```bash
# Make sure you're in virtual environment
source /home/meenvstf/virtualenv/public_html/sumithrakp/3.9/bin/activate
cd /home/meenvstf/public_html/sumithrakp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test the configuration
python manage.py check --deploy
```

## Step 8: Configure Static Files

1. In cPanel File Manager, create `.htaccess` in `/home/meenvstf/public_html/sumithrakp/`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_URI} !^/static/
RewriteCond %{REQUEST_URI} !^/media/
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [L]

# Serve static files directly
Alias /static /home/meenvstf/public_html/sumithrakp/staticfiles
Alias /media /home/meenvstf/public_html/sumithrakp/media
```

## Step 9: Restart Application

In Python App settings:
1. Click "Restart"

Or touch the passenger file:
```bash
touch /home/meenvstf/public_html/sumithrakp/passenger_wsgi.py
```

## Step 10: Set up Auto-Deployment (Optional)

1. In Git Version Control → Manage → Pull or Deploy
2. Copy the webhook URL
3. Go to GitHub repository → Settings → Webhooks
4. Add webhook:
   - Payload URL: [webhook URL from cPanel]
   - Content type: application/json
   - Events: Just the push event
5. Save webhook

## Future Updates Workflow

After initial setup, updating is simple:

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Update description"
git push origin main
```

3. If auto-deploy is set up: Changes deploy automatically
4. If manual: Go to cPanel Git → Pull or Deploy → Deploy HEAD Commit

## Troubleshooting

### Site shows 503 Error
- Check Python app is started
- Check passenger_wsgi.py path is correct
- Review error logs in cPanel

### Database Connection Error
- Verify MySQL credentials in .env
- Check database exists and user has permissions

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check .htaccess configuration
- Verify STATIC_ROOT path

### Import Errors
- Ensure all packages in requirements.txt are installed
- Check Python version compatibility

## Important Files Checklist

- [ ] `.env` created in production (NOT in Git)
- [ ] `passenger_wsgi.py` with correct paths
- [ ] `requirements.txt` with all dependencies
- [ ] `.gitignore` excludes sensitive files
- [ ] Database configured and migrated
- [ ] Static files collected
- [ ] Superuser created