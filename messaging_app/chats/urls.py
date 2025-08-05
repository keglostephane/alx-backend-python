from django.urls import include, path
from rest_framework_nested import routers

from .views import ConversationViewSet, MessageViewSet

# /conversations/
# /conversations/conversation_id/
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# /conversations/conversation_id/messages
conversations_router = routers.NestedDefaultRouter(router,
                                                   r"conversations",
                                                   lookup="conversation")
conversations_router.register(r"messages",
                              MessageViewSet,
                              basename="conversation-messages")

# /messages/
# /messages/message_id/
messages_router = routers.DefaultRouter()
messages_router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(conversations_router.urls)),
    path(r"", include(messages_router.urls)),
    path(r"messages/conversations/<str:conversation_id>",
         MessageViewSet.as_view({"get": "messages_by_conversation"}),
         name="messages-conversation-list")
]
