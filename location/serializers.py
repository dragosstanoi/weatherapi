from rest_framework import serializers
from .models import Location,Parameter


class LocationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'location_name',
            'description',
            'created_at',
            'lastupdate_at',
            'location_avail_params',
        ]

class LocationAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DetailLocationSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField('get_username')
    
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id', 'location_name', 'location_lat', 'location_lon', 'user', 'location_avail_params']

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

class LocationAddParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'

class LocationParameterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
