from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import *


class ContactSerializer(serializers.ModelSerializer):
    phone_number = serializers.RegexField(r'[0-9a-dA-D+*#]+', max_length=18, label="Номер телефона",
                                          validators=[UniqueValidator(queryset=Contact.objects.all())])
    email = serializers.EmailField(max_length=100, allow_null=True, label="Адрес электронной почты",
                                   validators=[UniqueValidator(queryset=Contact.objects.all())])

    class Meta:
        model = Contact
        fields = '__all__'
        validators = [UniqueTogetherValidator(queryset=Contact.objects.all(), fields=['first_name', 'last_name'])]


__all__ = ('ContactSerializer',)
