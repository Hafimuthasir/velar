from rest_framework import serializers
from .models import BussinessRequest
from djapp.models import User
from djapp.serializer import UserSerializers



class BussinessSerializer(serializers.ModelSerializer):
    # usse = UserSerializers(many=True)
    class Meta:
        model = BussinessRequest
        depth = 1
        fields = '__all__'