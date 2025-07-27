from django.urls import include, path
from rest_framework_nested import routers

from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

messages_router = routers.NestedDefaultRouter(router,
                                              r"conversations",
                                              lookup="conversation")
messages_router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(messages_router.urls))
]
