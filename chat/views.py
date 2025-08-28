from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from collections import defaultdict
from django.contrib.auth.decorators import login_required

from chat.models import ChatMessage

from collections import OrderedDict

from django.db.models import Q

User = get_user_model()

@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Fetch chat history (2-way conversation)
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    if request.method == "POST":
        msg = request.POST.get("message")
        if msg:
            ChatMessage.objects.create(sender=request.user, receiver=other_user, message=msg)
            return redirect("chat_with_user", user_id=other_user.id)

    return render(request, "main/chat_with_user.html", {
        "other_user": other_user,
        "messages": messages
    })


# chats/views.py


from django.shortcuts import render
from django.db.models import Q
from collections import OrderedDict
from chat.models import ChatMessage
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    """
    Show one row per conversation partner (whoever the user has chatted with),
    with the latest message preview and timestamp.
    Also marks all received messages as read to update notification count.
    """
    # Query all messages where user is sender or receiver
    qs = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').order_by('-timestamp')

    # Mark all received messages as read
    ChatMessage.objects.filter(receiver=request.user, is_read=False).update(is_read=True)

    threads = OrderedDict()
    for msg in qs:
        partner = msg.receiver if msg.sender == request.user else msg.sender
        # Only keep the latest message per partner (qs is already newest-first)
        if partner.id not in threads:
            threads[partner.id] = {
                "partner": partner,
                "last_message": msg.message,
                "last_time": msg.timestamp,
                "last_sender": msg.sender,
            }

    conversations = list(threads.values())
    return render(request, "main/inbox.html", {"conversations": conversations})



