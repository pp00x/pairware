from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/confirm/<int:item_id>/', views.confirm_transaction, name='confirm_transaction'),
    path('messages/send/<int:item_id>/', views.send_message, name='send_message'),
    path('messages/inbox/', views.inbox, name='inbox'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('username-recovery/', views.username_recovery, name='username_recovery'),
    path('username-recovery/done/', TemplateView.as_view(template_name='registration/username_recovery_done.html'), name='username_recovery_done'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
]