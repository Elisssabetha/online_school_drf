from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from app_course.models import Course, Lesson
from app_course.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """Viewset for Course model"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """View to create a lesson"""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """View to get a list of lessons"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """View to get a singe lesson by id"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """View to edit a lesson by id"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """View to delete a lesson by id"""
    queryset = Lesson.objects.all()
