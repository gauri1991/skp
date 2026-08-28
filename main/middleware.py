"""Middleware for running behind the cPanel/LiteSpeed reverse proxy.

Production traffic reaches Django as:

    Internet -> LiteSpeed (terminates TLS, .htaccess proxy)
             -> gunicorn on 127.0.0.1:8090 -> Django

``mod_proxy`` rewrites the ``Host`` header to the proxy *target* unless
``ProxyPreserveHost On`` is set, and that directive is only valid in server /
virtual-host config -- not in ``.htaccess``, which is the only Apache config
we control on shared hosting. So Django sees ``127.0.0.1:8090`` as the host,
which shows up two ways:

* every absolute URL is built from it -- ``<link rel="canonical">``,
  ``sitemap.xml``, password-reset links -- so the public site advertises
  ``http://127.0.0.1:8090/...``;
* CSRF checks fail on POST: the browser sends ``Origin:
  https://sumithrakp.com`` while Django believes it is serving
  ``http://127.0.0.1:8090``, and the two don't match.

``CanonicalHostMiddleware`` puts the public host and scheme back before
anything else reads them. It only ever rewrites requests that arrived on a
loopback address, i.e. from the local proxy -- gunicorn binds to 127.0.0.1,
so nothing else can reach it.
"""

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed


def _strip_port(host):
    """Return ``host`` without its port, handling IPv6 literals."""
    host = host.strip().lower()
    if host.startswith('['):  # IPv6 literal, e.g. [::1]:8090
        return host.partition(']')[0].lstrip('[')
    if host.count(':') == 1:  # name/IPv4 with a port
        return host.rpartition(':')[0]
    return host


def _is_loopback(host):
    """True when the request was addressed to the local gunicorn socket."""
    host = _strip_port(host)
    return (
        not host
        or host in {'localhost', '::1', '0.0.0.0'}
        or host.startswith('127.')
    )


class CanonicalHostMiddleware:
    """Rewrite the loopback proxy host back to the site's public host.

    Must be listed first in ``MIDDLEWARE`` so that ALLOWED_HOSTS validation,
    ``SecurityMiddleware``'s SSL redirect, CSRF origin checks and every
    ``build_absolute_uri()`` call downstream all see the public host.

    Reads ``settings.CANONICAL_HOST`` (required -- the middleware disables
    itself when it is empty) and ``settings.CANONICAL_PROTO`` (default
    ``https``). A proxy-supplied ``X-Forwarded-Host`` wins over
    ``CANONICAL_HOST`` when present, so the same code serves both apex and
    ``www`` correctly.
    """

    def __init__(self, get_response):
        self.canonical_host = getattr(settings, 'CANONICAL_HOST', '').strip()
        if not self.canonical_host:
            raise MiddlewareNotUsed
        self.canonical_proto = getattr(settings, 'CANONICAL_PROTO', 'https')
        self.get_response = get_response

    def __call__(self, request):
        if _is_loopback(request.META.get('HTTP_HOST', '')):
            forwarded = request.META.get('HTTP_X_FORWARDED_HOST', '')
            # A proxy chain may append to the header; the client-facing host
            # is the first entry.
            public_host = forwarded.split(',')[0].strip() or self.canonical_host
            request.META['HTTP_HOST'] = public_host
            # TLS is terminated at the edge, so the proxied request is plain
            # HTTP. Only fill in the scheme the proxy did not tell us about.
            request.META.setdefault('HTTP_X_FORWARDED_PROTO', self.canonical_proto)
        return self.get_response(request)
