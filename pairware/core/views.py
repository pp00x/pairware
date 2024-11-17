from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model  # Use this instead of User
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django import forms

from .forms import CustomUserCreationForm, ItemForm, MessageForm
from .models import Item, Message, UserRanking, Notification, CustomUser

# Get the custom user model
User = get_user_model()

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item posted successfully.')
            return redirect('item_list')
    else:
        form = ItemForm()
    categories = Item.objects.values_list('category', flat=True).distinct()
    return render(request, 'core/item_form.html', {'form': form, 'categories': categories})

def item_list(request):
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(
            Q(category__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-date_posted')
    else:
        items = Item.objects.all().order_by('-date_posted')
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/item_list.html', {'page_obj': page_obj, 'query': query})

@login_required
def send_message(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    recipient = item.owner
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.item = item
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'core/send_message.html', {'form': form, 'recipient': recipient, 'item': item})

@login_required
def inbox(request):
    messages_received = request.user.received_messages.all().order_by('-timestamp')
    messages_received.update(is_read=True)
    return render(request, 'core/inbox.html', {'messages': messages_received})

@login_required
def confirm_transaction(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user == item.owner:
        if request.method == 'POST':
            ranking, created = UserRanking.objects.get_or_create(user=request.user)
            ranking.items_given += 1
            ranking.save()
            
            # Update: Use get_user_model() here
            interested_users = User.objects.filter(sent_messages__item=item).distinct()
            for user in interested_users:
                Notification.objects.create(
                    user=user,
                    message=f"The item '{item.category} - {item.description}' has been confirmed by the owner."
                )
            
            item.delete()
            messages.success(request, 'Transaction confirmed and item removed.')
            return redirect('item_list')
        return render(request, 'core/confirm_transaction.html', {'item': item})
    else:
        return HttpResponseForbidden()

def leaderboard(request):
    rankings = UserRanking.objects.order_by('-items_given', '-requests_fulfilled')
    return render(request, 'core/leaderboard.html', {'rankings': rankings})

def username_recovery(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)  # Updated to use User = get_user_model()
            send_mail(
                'Username Recovery',
                f'Your username is {user.username}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'An email with your username has been sent.')
            return redirect('username_recovery_done')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'registration/username_recovery.html')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    items = Item.objects.filter(owner=user).order_by('-date_posted')
    try:
        ranking = UserRanking.objects.get(user=user)
    except UserRanking.DoesNotExist:
        ranking = None
    return render(request, 'core/user_profile.html', {
        'profile_user': user,
        'items': items,
        'ranking': ranking,
    })

@login_required
def notifications_view(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-timestamp')
    notifications.update(is_read=True)
    return render(request, 'core/notifications.html', {'notifications': notifications})
