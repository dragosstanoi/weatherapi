from rest_framework import serializers
from .models import Location,Parameter


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'location_name',
            'description',
            'created_at',
            'lastupdate_at'
        ]

class DetailLocationSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField('get_username')
    
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id', 'location_name', 'location_lat', 'location_lat', 'user']

    def get_username(self, location):
        user = location.user.username
        return user

    
    
class LocationParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = [
            'id',
            'name',
            'location',
            'unitsofmeasurment',
            'parameter_key_name'
        ]

class LocationParameterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
