from django.urls import include, path
from rest_framework import routers
from api.viewsets import NepenthesViewSet

router = routers.DefaultRouter()



# Wire up our API using automatic URL routing.
urlpatterns = [
    path('nepenthes/', NepenthesViewSet.as_view()),
]
# Additionally, we include login URLs for the browsable API.
