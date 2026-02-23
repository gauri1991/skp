from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Service


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'resume', 'portfolio', 'services', 'contact']

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Sitemap for project/portfolio items."""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('project_detail', kwargs={'slug': obj.slug})


class ServiceSitemap(Sitemap):
    """Sitemap for services."""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('service_inquiry', kwargs={'slug': obj.slug})
