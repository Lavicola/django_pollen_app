from django.db.models import Q

from pollen_app.models import Nepenthes, Feedback
from .serializers import NepenthesSerializer, FeedbackSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from pollen_app.models import SEX, FLOWER


class NepenthesViewSet(APIView):

    def get(self, request):
        '''
        List every nepenthes entry.
        '''
        sex = self.request.query_params.get('sex', None)
        flower_status = self.request.query_params.get('flower_status', None)
        isHybrid = self.request.query_params.get('isHybrid', None)  # 0 = false
        nepenthes = Nepenthes.objects.filter(~Q(flower=0))
        if (sex != None):
            if (sex == SEX.MALE):
                nepenthes = Nepenthes.objects.filter(sex=SEX.MALE)
            else:
                nepenthes = Nepenthes.objects.filter(sex=SEX.FEMALE)
        if (flower_status != None):
            if (flower_status == FLOWER.SOON_FLOWERING):
                nepenthes = Nepenthes.objects.filter(flower=FLOWER.SOON_FLOWERING)
            else:
                nepenthes = Nepenthes.objects.filter(flower=FLOWER.FLOWERS)
        if (isHybrid != None):
            if (isHybrid == False):
                nepenthes = Nepenthes.objects.filter(isHybrid=False)
            else:
                nepenthes = Nepenthes.objects.filter(isHybrid=True)


        serializer = NepenthesSerializer(nepenthes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
