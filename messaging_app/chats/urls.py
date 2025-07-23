from django.urls import include, path
from rest_framework import routers

from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"conversations", ConversationViewSet, basename="conversation")

urlpatterns = [path('', include(router.urls))]
