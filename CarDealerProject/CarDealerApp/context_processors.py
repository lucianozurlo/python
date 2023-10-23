import os
from django.conf import settings
from django.contrib.auth.context_processors import auth
from accounts.models import Avatar

def custom_user(request):
    context = auth(request)
    user = context['user']

    if user.is_authenticated:
        context['user_name'] = request.user.username
        avatar = Avatar.objects.filter(user=request.user.id)
        cant = len(avatar)
        if cant > 0:
            context['avatar_image'] = avatar[cant-1]
        else:
            context['avatar_image'] = os.path.join(settings.MEDIA_URL, 'avatars', 'generic.jpg')

    return context
