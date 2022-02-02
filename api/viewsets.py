from pollen_app.models import Nepenthes,Feedback
from .serializers import NepenthesSerializer,FeedbackSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status








class NepenthesViewSet(APIView):


    def get(self, request):
        '''
        List every nepenthes entry.
        '''
        nepenthes = Nepenthes.objects.all()
        serializer = NepenthesSerializer(nepenthes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT API for the webservice try. NOT SECURE and just here to show it could be done.
    def post(self, request):
        serializer = NepenthesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackViewSet(APIView):


    def get(self, request):
        '''
        List every Feedback entry.
        '''
        nepenthes = Feedback.objects.all()
        serializer = FeedbackSerializer(nepenthes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT API for the webservice try. NOT SECURE and just here to show it could be done.
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


