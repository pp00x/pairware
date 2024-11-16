def unread_messages_count(request):
    if request.user.is_authenticated:
        count = request.user.received_messages.filter(is_read=False).count()
        return {'unread_messages_count': count}
    return {}

def notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        return {'notifications': notifications}
    return {}

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
        return {'unread_notifications_count': count}
    return {}