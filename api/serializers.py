from rest_framework import serializers
from pollen_app.models import Nepenthes, Feedback
from user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username",)


class NepenthesSerializer(serializers.ModelSerializer):
    username = CustomUserSerializer(
        source='getUsername',
        read_only=True
    )
    class Meta:
        model = Nepenthes
        fields = ('id', 'name', 'flower', "username", "sex", "isHybrid", 'image', 'description')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("__all__")
