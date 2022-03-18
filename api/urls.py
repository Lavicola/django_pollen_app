from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import TransactionView,NepenthesView,NepenthesEditView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('nepenthes/', (NepenthesView.as_view())),
    path('nepenthes/edit/', NepenthesEditView.as_view()),
    path('transaction', TransactionView.as_view()),
]
