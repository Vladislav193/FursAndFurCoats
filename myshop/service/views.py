import json
import secrets

from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from Users.models import User
from django.contrib.auth import login

def sercret_token(request):
    unique_token = secrets.token_urlsafe()
    cache.set(unique_token, unique_token, timeout=300)
    return render(request, 'login.html', {'unique_token':unique_token})


def telega_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        telega_id = data.get('telegram_id')
        auth_token = data.get('auth_token')
        token = cache.get('unique_token')
        if auth_token != token :
            return JsonResponse({'error': 'Invalid token'}, status=400)
        cache.delete('unique_token')
        user, created = User.objects.get_or_created(telega_id=telega_id)
        if created:
            user.username = data.get('telegram_username')
            user.last_name =  data.get('telegram_last_name')
            user.first_name = data.get('telegram_first_name')
            user.email = data.get('telegram_email')
            user.telega_id = telega_id
            user.save
        login(request, user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
