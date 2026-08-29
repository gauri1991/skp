from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.test import RequestFactory, SimpleTestCase, override_settings

from main.middleware import CanonicalHostMiddleware

# Mirrors production: the site is public at https://sumithrakp.com but
# gunicorn receives the proxied request as Host: 127.0.0.1:8090.
PROXY_SETTINGS = {
    'CANONICAL_HOST': 'sumithrakp.com',
    'CANONICAL_PROTO': 'https',
    'ALLOWED_HOSTS': ['sumithrakp.com', 'www.sumithrakp.com', '127.0.0.1'],
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'CSRF_TRUSTED_ORIGINS': ['https://sumithrakp.com', 'https://www.sumithrakp.com'],
}


def echo(request):
    return request


@override_settings(**PROXY_SETTINGS)
class CanonicalHostMiddlewareTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = CanonicalHostMiddleware(echo)

    def test_loopback_host_is_replaced_with_canonical_host(self):
        request = self.middleware(self.factory.get('/services/', HTTP_HOST='127.0.0.1:8090'))
        self.assertEqual(request.get_host(), 'sumithrakp.com')
        self.assertTrue(request.is_secure())
        self.assertEqual(
            request.build_absolute_uri(),
            'https://sumithrakp.com/services/',
        )

    def test_forwarded_host_wins_over_canonical_host(self):
        request = self.middleware(self.factory.get(
            '/',
            HTTP_HOST='127.0.0.1:8090',
            HTTP_X_FORWARDED_HOST='www.sumithrakp.com',
        ))
        self.assertEqual(request.get_host(), 'www.sumithrakp.com')

    def test_the_nearest_proxys_entry_wins_in_a_forwarded_host_chain(self):
        # LiteSpeed appends what it saw, so the trustworthy entry is the last
        # one; the loopback target it proxies to is skipped.
        request = self.middleware(self.factory.get(
            '/',
            HTTP_HOST='127.0.0.1:8090',
            HTTP_X_FORWARDED_HOST='sumithrakp.com, 127.0.0.1:8090',
        ))
        self.assertEqual(request.get_host(), 'sumithrakp.com')

    def test_spoofed_forwarded_host_falls_back_to_the_canonical_host(self):
        # A client can write X-Forwarded-Host itself. Anything ALLOWED_HOSTS
        # would reject is ignored rather than passed through to raise 400.
        request = self.middleware(self.factory.get(
            '/',
            HTTP_HOST='127.0.0.1:8090',
            HTTP_X_FORWARDED_HOST='evil.example',
        ))
        self.assertEqual(request.get_host(), 'sumithrakp.com')

    def test_spoofed_entry_cannot_outrank_the_real_one(self):
        request = self.middleware(self.factory.get(
            '/',
            HTTP_HOST='127.0.0.1:8090',
            HTTP_X_FORWARDED_HOST='evil.example, www.sumithrakp.com',
        ))
        self.assertEqual(request.get_host(), 'www.sumithrakp.com')

    def test_public_host_is_left_alone(self):
        request = self.middleware(self.factory.get('/', HTTP_HOST='www.sumithrakp.com'))
        self.assertEqual(request.get_host(), 'www.sumithrakp.com')
        # Nothing arrived on loopback, so the scheme is not assumed either.
        self.assertNotIn('HTTP_X_FORWARDED_PROTO', request.META)

    def test_client_supplied_scheme_cannot_downgrade_the_request(self):
        # X-Forwarded-Proto reaches Django verbatim from the client here, so
        # it must not be able to clear is_secure(). The edge redirects http
        # to https, so a proxied request is always https.
        request = self.middleware(self.factory.get(
            '/',
            HTTP_HOST='127.0.0.1:8090',
            HTTP_X_FORWARDED_PROTO='http',
        ))
        self.assertTrue(request.is_secure())

    def test_localhost_and_ipv6_loopback_are_recognised(self):
        for host in ('localhost:8090', 'localhost', '[::1]:8090', '127.0.0.2'):
            with self.subTest(host=host):
                request = self.middleware(self.factory.get('/', HTTP_HOST=host))
                self.assertEqual(request.get_host(), 'sumithrakp.com')

    @override_settings(CANONICAL_HOST='')
    def test_middleware_disables_itself_without_a_canonical_host(self):
        from django.core.exceptions import MiddlewareNotUsed

        with self.assertRaises(MiddlewareNotUsed):
            CanonicalHostMiddleware(echo)


@override_settings(**PROXY_SETTINGS)
class CsrfOriginTests(SimpleTestCase):
    """The regression: POSTs failed the CSRF origin check behind the proxy."""

    def setUp(self):
        self.factory = RequestFactory()
        self.csrf = CsrfViewMiddleware(echo)

    def _post(self, origin):
        token = get_token(self.factory.get('/'))
        request = self.factory.post(
            '/contact/',
            {'csrfmiddlewaretoken': token},
            HTTP_HOST='127.0.0.1:8090',
            HTTP_ORIGIN=origin,
        )
        request.COOKIES['csrftoken'] = token
        return request

    @override_settings(CSRF_TRUSTED_ORIGINS=[])
    def test_origin_is_rejected_when_the_proxy_host_leaks_through(self):
        # Pre-fix state: Django compares Origin against its own host, sees
        # http://127.0.0.1:8090, and has no trusted origin to fall back on.
        response = self.csrf.process_view(self._post('https://sumithrakp.com'), echo, (), {})
        self.assertEqual(response.status_code, 403)

    @override_settings(CSRF_TRUSTED_ORIGINS=[])
    def test_middleware_alone_satisfies_the_origin_check(self):
        request = CanonicalHostMiddleware(echo)(self._post('https://sumithrakp.com'))
        self.assertIsNone(self.csrf.process_view(request, echo, (), {}))

    def test_origin_is_accepted_behind_the_proxy(self):
        request = CanonicalHostMiddleware(echo)(self._post('https://sumithrakp.com'))
        self.assertIsNone(self.csrf.process_view(request, echo, (), {}))

    def test_www_origin_is_accepted_via_trusted_origins(self):
        request = CanonicalHostMiddleware(echo)(self._post('https://www.sumithrakp.com'))
        self.assertIsNone(self.csrf.process_view(request, echo, (), {}))

    def test_spoofed_forwarded_host_cannot_make_an_origin_trusted(self):
        request = self._post('https://evil.example')
        request.META['HTTP_X_FORWARDED_HOST'] = 'evil.example'
        request = CanonicalHostMiddleware(echo)(request)
        self.assertEqual(self.csrf.process_view(request, echo, (), {}).status_code, 403)

    def test_unrelated_origin_is_still_rejected(self):
        request = CanonicalHostMiddleware(echo)(self._post('https://evil.example'))
        self.assertEqual(self.csrf.process_view(request, echo, (), {}).status_code, 403)


class ProductionSettingsTests(SimpleTestCase):
    """Guard the production defaults that keep the proxied site consistent."""

    #: Env vars that override the defaults under test; production sets them
    #: from ~/app_env.sh, so they are scrubbed before importing the module.
    ENV_OVERRIDES = (
        'CANONICAL_HOST',
        'CANONICAL_PROTO',
        'ALLOWED_HOSTS',
        'CSRF_TRUSTED_ORIGINS',
        'SECURE_SSL_REDIRECT',
    )

    def setUp(self):
        import importlib
        import os
        from unittest import mock

        with mock.patch.dict(os.environ):
            for name in self.ENV_OVERRIDES:
                os.environ.pop(name, None)
            self.prod = importlib.reload(importlib.import_module('settings_production'))

    def test_canonical_middleware_runs_first(self):
        self.assertEqual(
            self.prod.MIDDLEWARE[0], 'main.middleware.CanonicalHostMiddleware'
        )

    def test_csrf_trusted_origins_default_to_the_public_https_origins(self):
        self.assertEqual(
            self.prod.CSRF_TRUSTED_ORIGINS,
            ['https://sumithrakp.com', 'https://www.sumithrakp.com'],
        )

    def test_allowed_hosts_defaults_cover_the_public_host(self):
        self.assertIn('sumithrakp.com', self.prod.ALLOWED_HOSTS)
        self.assertIn('www.sumithrakp.com', self.prod.ALLOWED_HOSTS)

    def test_ssl_redirect_is_left_to_the_edge(self):
        # gunicorn only ever sees plain HTTP; redirecting here loops.
        self.assertFalse(self.prod.SECURE_SSL_REDIRECT)
        self.assertEqual(
            self.prod.SECURE_PROXY_SSL_HEADER, ('HTTP_X_FORWARDED_PROTO', 'https')
        )
