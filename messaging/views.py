from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def chat_view(request, user_id):

    # Prevent user chatting with themselves
    if request.user.id == user_id:
        return redirect('home')

    receiver = get_object_or_404(User, id=user_id)

    # Fetch conversation
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    )

    # Send new message
    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text.strip():
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message_text.strip()
            )

        return redirect('chat', user_id=receiver.id)

    context = {
        'messages': messages,
        'receiver': receiver
    }

    return render(request, 'messaging/chat.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def chat_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    # AJAX Request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'messaging/messages_partial.html',
            {'messages': messages, 'request': request}
        )
        return JsonResponse({'html': html})

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message_text
            )
        return redirect('chat', user_id=receiver.id)

    return render(request, 'messaging/chat.html', {
        'messages': messages,
        'receiver': receiver
    })
