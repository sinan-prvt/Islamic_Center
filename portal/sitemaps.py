from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'about',
            'committee',
            'programs',
            'gallery',
            'news',
            'contact',
            'monthly_fund',
            'donate',
            'transparency',
            'check_contribution',
        ]

    def location(self, item):
        return reverse(item)
