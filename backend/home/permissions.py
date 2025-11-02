"""
Custom Permission Classes for SmartRecommender API.

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0

This module defines custom permission classes for Django REST Framework
to control access based on user roles (admin, client).
"""

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
