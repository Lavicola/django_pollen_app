from django.db import IntegrityError
from django.db.models import Q
import json

from django.http import HttpResponse,JsonResponse
from pollen_app.models import Nepenthes, Feedback, Transaction
from .Validator import validate_transaction
from .forms import MyValidationForm
from .serializers import NepenthesSerializer, FeedbackSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from pollen_app.models import SEX, FLOWER
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from user.models import CustomUser


class NepenthesView(APIView):

    def get(self, request):
        '''
        List every nepenthes entry.
        '''
        if request.user.is_authenticated:
            nepenthes = Nepenthes.objects.exclude(owner_id=request.user.id)
            serializer = NepenthesSerializer(nepenthes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



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


class TransactionView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            author_id = request.user.id
            transactions = Transaction.objects.filter(author_id=author_id) .select_related("nepenthes")#all transaction offers




        return Response()

    def post(self, request):

        if request.user.is_authenticated:
            user_plant_id = request.POST.get('user_plant_id')  # the plant he selected in the dropdown menu
            author_plant_id = request.POST.get('author_plant_id')  # id of the plant of the post
            author = request.POST.get('author')  # username of the author
            author_id = validate_transaction(request.user.id, user_plant_id, author,
                                             author_plant_id)  # not just validating...
            try:
                transaction = Transaction(author_id=author_id, author_plant_id=author_plant_id, user_id=request.user.id,
                                          user_plant_id=user_plant_id)
                transaction.save()
            except IntegrityError as e:
                return Response(status=409)

            return Response(status=201)

        return Response(status=500)

    def put(self, request):
        if request.user.is_authenticated:
            transactionId = request.POST.get("transactionId");
            accepted = request.POST.get("accepted");
            if accepted ==  "true":
                accepted = True
            elif accepted == "false":
                accepted = False
            else:
                return Response(status=409)
            try:
                transaction = Transaction.objects.filter(id=transactionId,accepted__isnull=True)
                transaction.update(accepted=accepted)
            except IntegrityError as e:
                return Response(status=409)

        if accepted:
            # TODO optimize
            transaction = Transaction.objects.filter(id=transactionId).first()
            user_id = transaction.user_id
            user_email = CustomUser.objects.filter(id=user_id).values_list('email', flat=True).first()
            response = JsonResponse({'mail': user_email}, status=201)
            return response
        else:
            return Response(status=201)










