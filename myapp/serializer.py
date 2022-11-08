from rest_framework import serializers
from .models import *


"""
user serializer
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email","username","full_name")



class Taskserializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields=('created_by',)


        