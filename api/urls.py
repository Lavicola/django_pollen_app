from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import TransactionView,NepenthesView


urlpatterns = [
    path('nepenthes/', NepenthesView.as_view()),
    path('transaction', TransactionView.as_view()),
]