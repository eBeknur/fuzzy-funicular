from rest_framework.serializers import ModelSerializer
from .models import Link


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'file' , 'views' ,'description', 'url')


