from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from app_course.models import Course, Lesson, Payment, Subscription
from app_course.pagination import CourseLessonPaginator
from app_course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsModerator


class CourseViewSet(ModelViewSet):
    """Viewset for Course model"""
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated & IsModerator]
        else:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """View to create a lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """View to get a list of lessons"""
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPaginator
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """View to get a singe lesson by id"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """View to edit a lesson by id"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsModerator]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """View to delete a lesson by id"""
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class PaymentListAPIView(generics.ListAPIView):
    """View to get a list of payments with ability to filter and order"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # фильтрация по полям .../payments/?course=1
    # Изменение последовательности .../course/?ordering=-payment_date
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """View to create a subscription"""
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """View to delete a subscription by id"""
    queryset = Subscription.objects.all()
