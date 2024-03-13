

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from task_management import settings
from .views import LabelViewSet, TaskViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router.register(r'labels', LabelViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
