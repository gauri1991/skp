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

### The proxy rewrites the Host header

`mod_proxy` replaces the `Host` header with the proxy target unless
`ProxyPreserveHost On` is set — and that directive is invalid in `.htaccess`,
the only Apache config we control here. So Django receives
`Host: 127.0.0.1:8090`, which used to leak into every absolute URL
(`<link rel="canonical">`, `sitemap.xml`, emailed links) and broke CSRF on every
POST: the browser sends `Origin: https://sumithrakp.com`, Django believed it
was serving `http://127.0.0.1:8090`, and the two didn't match.

Two halves fix it, and either half works alone:

1. `htaccess-proxy.txt` forwards `X-Forwarded-Host` / `X-Forwarded-Proto`.
2. `main.middleware.CanonicalHostMiddleware` (first in `MIDDLEWARE`) restores
   the public host on any request that arrived on loopback — from
   `X-Forwarded-Host` when present, otherwise from the `CANONICAL_HOST`
   setting, which defaults to `sumithrakp.com` and is overridable via
   `app_env.sh`. It also marks those requests as https, which
   `SECURE_PROXY_SSL_HEADER` turns into `request.is_secure()`.

`ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` both default to the canonical host
(plus `www.`) in `settings_production.py`, so a missing `app_env.sh` export no
longer takes the site down. Regression tests: `manage.py test main`.

## Recovery: the three server-only pieces

If the server is ever wiped, restore these after re-cloning the repo and
reinstalling `requirements_production.txt` into the virtualenv:

### 1. `~/app_env.sh` — secrets (copy `app_env.sh.example`, fill in real values)

### 2. `~/public_html/.htaccess` — prepend the contents of `htaccess-proxy.txt`
above whatever cPanel has generated there.

### 3. Keepalive cron job (cPanel → Cron Jobs, every minute: `* * * * *`):

```
. /home/meenvstf/app_env.sh; cd /home/meenvstf/repositories/skp && git pull -q origin main 2>/dev/null; kill -0 $(cat /home/meenvstf/gunicorn.pid 2>/dev/null) 2>/dev/null || /home/meenvstf/virtualenv/repositories/skp/3.11/bin/gunicorn --chdir /home/meenvstf/repositories/skp -w 2 --threads 8 --timeout 180 -b 127.0.0.1:8090 --daemon --pid /home/meenvstf/gunicorn.pid passenger_wsgi:application >> /home/meenvstf/gunicorn_cron.log 2>&1
```

### 4. AI job worker cron (every minute):

```
* * * * * . /home/meenvstf/app_env.sh; /home/meenvstf/virtualenv/repositories/skp/3.11/bin/python /home/meenvstf/repositories/skp/manage.py process_ai_jobs >> /home/meenvstf/ai_jobs.log 2>&1
```

(Threaded gunicorn — `--threads 8 --timeout 180` — is required so synchronous AI
calls don't starve the two workers.)

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
- `SECURE_SSL_REDIRECT` must stay `False` (LiteSpeed terminates TLS; gunicorn
  sees plain HTTP and would redirect-loop). The http -> https redirect lives in
  `.htaccess` instead — it is part of `htaccess-proxy.txt`.
- `media/` is not in git; content added via the dashboard lives only in
  production (MySQL + `~/repositories/skp/media/`). Back those up separately.
