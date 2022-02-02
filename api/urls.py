from django.urls import include, path
from rest_framework import routers
from api.viewsets import NepenthesViewSet,FeedbackViewSet

router = routers.DefaultRouter()



# Wire up our API using automatic URL routing.
urlpatterns = [
    path('nepenthes/', NepenthesViewSet.as_view()),
    path('feedback/', FeedbackViewSet.as_view()),
]
# Additionally, we include login URLs for the browsable API.
