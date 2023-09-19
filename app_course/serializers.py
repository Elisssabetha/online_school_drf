from rest_framework import serializers

from app_course.models import Course, Lesson, Payment, Subscription
from app_course.services import get_payment_link
from app_course.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)
    subscription_status = serializers.SerializerMethodField()
    # payment_link = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        """qty of lessons in the course"""
        return instance.lesson.count()

    # def get_payment_link(self, instance):
    #     payment_data = get_payment_link(instance)
    #     return payment_data['url']

    def get_subscription_status(self, instance):
        request = self.context.get('request')
        subscription = Subscription.objects.filter(course=instance, user=request.user).first()
        if subscription:
            return subscription.status
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
