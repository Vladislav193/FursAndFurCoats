import os
import requests
from dotenv import load_dotenv
from rest_framework import serializers
from .models import User

load_dotenv()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = ["username", "first_name", "last_name", "email", "password"]


    def validate_email(self, email):
        url = "https://dadata.ru/api/v2/clean/email"
        dadata_api_key = os.getenv('DADATA_API_KEY')
        headers = {
            "Authorization": f"Token {dadata_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=[email], headers=headers)

        if response.status_code == 200:
            clean_data = response.json()
            corrected_email = clean_data[0].get("email", None)
            if corrected_email:
                email = corrected_email
        else:
            raise serializers.ValidationError("Не удалось проверить email через DaData.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже есть")
        return email