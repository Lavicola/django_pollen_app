from rest_framework import serializers
from pollen_app.models import Nepenthes,Feedback




class NepenthesSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Nepenthes
        fields=('id','name','inflorescence','image','description')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("__all__")
