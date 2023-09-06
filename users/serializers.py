from rest_framework import serializers

from app_course.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'city', 'avatar', 'payments')
