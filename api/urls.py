from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import TransactionView, NepenthesView, NepenthesEditView

urlpatterns = [
    path('nepenthes/', (NepenthesView.as_view())),
    path('nepenthes/edit/<int:pk>', NepenthesEditView.as_view()),
    path('transaction', TransactionView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
