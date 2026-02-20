from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import User, Message

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('user_list')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            user.is_online = True
            user.save()
            return redirect('user_list')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    from django.utils import timezone
    request.user.is_online = False
    request.user.last_seen = timezone.now()
    request.user.save()
    logout(request)
    return redirect('login')

@login_required
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    users_with_unread = []
    for u in users:
        unread_count = Message.objects.filter(sender=u, receiver=request.user, is_read=False).count()
        users_with_unread.append({'user': u, 'unread_count': unread_count})
    return render(request, 'user_list.html', {'users_data': users_with_unread})

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    )
    
    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages_list
    })

@login_required
def delete_message_view(request, message_id):
    if request.method == 'POST':
        try:
            message = Message.objects.get(id=message_id, sender=request.user)
            message.delete()
            return JsonResponse({'status': 'success'})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
