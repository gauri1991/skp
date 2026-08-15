# Production Deployment — Razorhost cPanel (sumithrakp.com)

Production does **not** use Passenger / "Setup Python App". LiteSpeed's Python
integration is broken on this server (`lscgid` wants a missing
`/usr/bin/lswsgi3` binary), so the site runs as:

```
Internet → LiteSpeed (.htaccess proxy) → gunicorn on 127.0.0.1:8090 → Django
```

- App code lives in `~/repositories/skp` (a git clone of this repo).
- gunicorn runs from the CloudLinux virtualenv at
  `~/virtualenv/repositories/skp/3.11/`, loading `passenger_wsgi:application`.
- A cron job (every minute) pulls from GitHub and restarts gunicorn if dead —
  so **pushing to `main` auto-deploys within a minute**. Code changes need a
  process restart to take effect: `kill $(cat ~/gunicorn.pid)` (the cron
  respawns it).

## Recovery: the three server-only pieces

If the server is ever wiped, restore these after re-cloning the repo and
reinstalling `requirements_production.txt` into the virtualenv:

### 1. `~/app_env.sh` — secrets (copy `app_env.sh.example`, fill in real values)

### 2. `~/public_html/.htaccess` — prepend the contents of `htaccess-proxy.txt`
above whatever cPanel has generated there.

### 3. Keepalive cron job (cPanel → Cron Jobs, every minute: `* * * * *`):

```
. /home/meenvstf/app_env.sh; cd /home/meenvstf/repositories/skp && git pull -q origin main 2>/dev/null; kill -0 $(cat /home/meenvstf/gunicorn.pid 2>/dev/null) 2>/dev/null || /home/meenvstf/virtualenv/repositories/skp/3.11/bin/gunicorn --chdir /home/meenvstf/repositories/skp -w 2 -b 127.0.0.1:8090 --daemon --pid /home/meenvstf/gunicorn.pid passenger_wsgi:application >> /home/meenvstf/gunicorn_cron.log 2>&1
```

Then run once (cPanel Terminal or a temporary cron):

```
. ~/app_env.sh
cd ~/repositories/skp
~/virtualenv/repositories/skp/3.11/bin/python manage.py migrate
~/virtualenv/repositories/skp/3.11/bin/python manage.py collectstatic --noinput
```

## Gotchas learned the hard way

- Do NOT use Stop/Restart in "Setup Python App" — the CloudLinux selector
  overwrites `passenger_wsgi.py` with a broken self-loading stub. If git pulls
  start failing with "uncommitted changes" on the server:
  `git checkout -- passenger_wsgi.py`.
- `settings_production.py` sits at the repo ROOT, so its `BASE_DIR` is
  `Path(__file__).resolve().parent` (NOT `.parent.parent`).
- The cron keepalive must check the PID file, not `pgrep` — `pgrep -f` matches
  the cron shell's own command line and never starts anything.
- `SECURE_SSL_REDIRECT` must be `False` in `app_env.sh` (LiteSpeed terminates
  TLS; gunicorn sees plain HTTP and would redirect-loop), and
  `CSRF_TRUSTED_ORIGINS` must list the https origins.
- `media/` is not in git; content added via the dashboard lives only in
  production (MySQL + `~/repositories/skp/media/`). Back those up separately.
