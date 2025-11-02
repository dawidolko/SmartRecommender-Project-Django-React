"""
Django Application Configuration for SmartRecommender Home Module.

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0

This module configures the 'home' Django app and registers signal handlers
for automatic recommendation updates and analytics generation.
"""

from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    
    def ready(self):
        import home.signals