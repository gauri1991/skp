# GitHub Integration with cPanel for Continuous Deployment

## Method 1: Git Version Control in cPanel (Recommended)

Most modern cPanel installations include Git Version Control. This is the easiest method.

### Setup Steps:

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/sumithrakp-website.git
   git push -u origin main
   ```

2. **In cPanel - Git Version Control**
   - Go to "Git Version Control" in cPanel
   - Click "Create"
   - Enter repository URL: `https://github.com/yourusername/sumithrakp-website.git`
   - Set repository path: `/home/cpanelusername/sumithrakp.com`
   - Click "Create"

3. **Set up Deploy Hook**
   - In Git Version Control, click "Manage" on your repo
   - Go to "Pull or Deploy" tab
   - Copy the deployment URL
   - Add this as a webhook in GitHub:
     - Go to GitHub repo → Settings → Webhooks
     - Add webhook with cPanel deployment URL
     - Set to trigger on push events

### Auto-Deployment Process:
1. Push changes to GitHub
2. GitHub triggers cPanel webhook
3. cPanel automatically pulls latest code
4. Your deployment script runs (migrations, static collection, etc.)

## Method 2: SSH and Git Pull

If your cPanel has SSH access:

### Initial Setup:

1. **SSH into your cPanel account**
   ```bash
   ssh cpanelusername@yourdomain.com
   ```

2. **Clone repository**
   ```bash
   cd ~/public_html  # or your app directory
   git clone https://github.com/yourusername/sumithrakp-website.git .
   ```

3. **Create deployment script**
   ```bash
   nano ~/deploy.sh
   ```

## Method 3: GitHub Actions with FTP

If cPanel doesn't have Git but has FTP:

### Setup GitHub Actions:

1. **Get FTP credentials from cPanel**
2. **Add secrets to GitHub repo**:
   - Go to Settings → Secrets → Actions
   - Add: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`

3. **Create workflow file** (see `.github/workflows/deploy.yml` below)

## Best Practices

### 1. Environment Variables
- Never commit `.env` to GitHub
- Store production `.env` directly on server
- Use cPanel's Environment Variables if available

### 2. Database
- Don't commit `db.sqlite3`
- Use MySQL in production
- Keep database backups

### 3. Static Files
- Don't commit `staticfiles/` directory
- Run `collectstatic` after deployment
- Use WhiteNoise or configure web server

### 4. Deployment Checklist
- [ ] Push code to GitHub
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Database migrations run automatically
- [ ] Static files collected
- [ ] Application restarted
- [ ] Test all functionality

## Troubleshooting

### Common Issues:

1. **Permission Denied**
   - Set correct file permissions: `chmod 755 -R .`
   - Ensure git has write access

2. **Module Not Found**
   - Reinstall requirements after pull: `pip install -r requirements.txt`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic --noinput`
   - Check static files path in cPanel

4. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Check database credentials in `.env`

## Zero-Downtime Deployment

To avoid disruption during updates:

1. **Use maintenance mode**
2. **Deploy during low-traffic hours**
3. **Use database migrations carefully**
4. **Test on staging first**
5. **Keep rollback plan ready**

## Rollback Strategy

If something goes wrong:

```bash
# Via SSH or cPanel Terminal
cd /home/cpanelusername/sumithrakp.com
git log --oneline -5  # See recent commits
git reset --hard <previous-commit-hash>  # Rollback
python manage.py migrate  # Re-run migrations if needed
python manage.py collectstatic --noinput
touch passenger_wsgi.py  # Restart app
```