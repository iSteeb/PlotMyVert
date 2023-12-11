from rest_framework import serializers
from .models import JumpSessionModel, JumpSessionJumpsModel

class JumpSessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpSessionModel
        fields = ['user', 'start_datetime', 'count', 'average_high', 'highest', 'plotly_json']

class JumpSessionJumpsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpSessionJumpsModel
        fields = ['session', 'timestamp', 'jump_height']