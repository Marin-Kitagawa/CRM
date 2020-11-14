from accounts.models import *
# Activity, Game, Tag, Patient
from rest_framework.serializers import ModelSerializer


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
