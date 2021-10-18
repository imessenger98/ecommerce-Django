from rest_framework import fields, serializers
from .models import User
from .models import order
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =order
        fields = "__all__"