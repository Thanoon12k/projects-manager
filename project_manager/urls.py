"""
URL configuration for project_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from projects.api_views import ProjectViewSet, ProjectTypeViewSet, ProjectImageViewSet, ProjectFileViewSet
from customers.api_views import CustomerViewSet
from payments.api_views import PaymentPartViewSet

# API Router
router = DefaultRouter()
router.register(r'api/projects', ProjectViewSet, basename='project')
router.register(r'api/project-types', ProjectTypeViewSet, basename='projecttype')
router.register(r'api/project-images', ProjectImageViewSet, basename='projectimage')
router.register(r'api/project-files', ProjectFileViewSet, basename='projectfile')
router.register(r'api/customers', CustomerViewSet, basename='customer')
router.register(r'api/payments', PaymentPartViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('customers/', include('customers.urls')),
    path('payments/', include('payments.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
