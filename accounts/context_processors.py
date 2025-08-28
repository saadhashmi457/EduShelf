

from notifications.models import Notification
from chat.models import ChatMessage

def global_counts(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
        unread_messages = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
        return {
            'global_unread_count': unread_notifications,
            'global_unread_messages': unread_messages
        }
    return {
        'global_unread_count': 0,
        'global_unread_messages': 0
    }
