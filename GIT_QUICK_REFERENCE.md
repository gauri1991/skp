# Git Quick Reference for Website Updates

## Initial Setup (One-time)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit"

# Add GitHub remote
git remote add origin https://github.com/yourusername/sumithrakp-website.git

# Push to GitHub
git push -u origin main
```

## Daily Workflow

### 1. Before Making Changes
```bash
# Check current status
git status

# Pull latest changes (if working from multiple locations)
git pull origin main
```

### 2. After Making Changes
```bash
# See what changed
git status

# Add specific files
git add filename.py
# OR add all changes
git add .

# Commit with descriptive message
git commit -m "Add new feature: contact form"

# Push to GitHub
git push origin main
```

### 3. Common Commands

```bash
# View recent commits
git log --oneline -10

# Undo last commit (before push)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename.py

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name
```

## cPanel Deployment Commands

### Via SSH/Terminal in cPanel:

```bash
# Navigate to website directory
cd ~/sumithrakp.com

# Pull latest changes
git pull origin main

# Run deployment script
./deploy.sh

# Manual deployment steps if needed:
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch passenger_wsgi.py  # Restart app
```

## Important Files to Never Commit

These should be in `.gitignore`:
- `.env` (contains secrets)
- `db.sqlite3` (local database)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `staticfiles/` (generated files)
- `media/` (user uploads)

## Emergency Rollback

If something breaks after deployment:

```bash
# In cPanel terminal
cd ~/sumithrakp.com

# View recent commits
git log --oneline -5

# Rollback to previous version
git reset --hard <commit-hash>

# Re-run deployment
./deploy.sh
```

## Best Practices

1. **Always test locally first**
   ```bash
   python manage.py runserver
   ```

2. **Write clear commit messages**
   - Good: "Fix contact form validation error"
   - Bad: "Fixed stuff"

3. **Commit frequently**
   - Small, focused commits are better
   - Easier to track and rollback

4. **Pull before push**
   - Avoid conflicts
   - Stay synchronized

5. **Never commit sensitive data**
   - Passwords
   - API keys
   - Secret keys

## Typical Update Workflow Example

```bash
# 1. Make your changes locally
# Edit files...

# 2. Test locally
python manage.py runserver
# Test your changes at http://127.0.0.1:8000

# 3. Commit and push
git add .
git commit -m "Update homepage content"
git push origin main

# 4. Deploy (automatic via webhook or manual in cPanel)
# Changes appear on live site!
```