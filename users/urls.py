from users.apps import UsersConfig
from app_course.apps import AppCourseConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [

] + router.urls
