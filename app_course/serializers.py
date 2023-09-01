from rest_framework import serializers

from app_course.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True)

    def get_lessons_count(self, instance):
        """qty of lessons in the course"""
        return instance.lesson.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
