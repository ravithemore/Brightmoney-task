from rest_framework import serializers
from .models import User, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ['user_id','name','email_id','annual_income']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
      model = Transaction
      fields = ['__all__']