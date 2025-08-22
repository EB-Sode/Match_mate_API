from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserStats

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

#Registeration serializer
class RegisterUser(serializers.ModelSerializer):
    '''Serializer for user registration'''
    
    password = serializers.CharField(write_only= True)

    class Meta:
        model = User 
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get['email'],
            password = validated_data['password']

        )
        return user

#Leaderboard serializer from userstats model. 
class LeaderboardSerializer(serializers.ModelSerializer):
    '''Serializer for the leaderboard views and rankings'''

    username = serializers.CharField(source="user.username", read_only=True)
    rank = serializers.SerializerMethodField()

    class Meta:
        model = UserStats
        fields = ["rank", "username", "total_points", "correct_predictions"]

    def get_rank(self, obj):
        # Find this user's position in the ordered queryset
        queryset = UserStats.objects.order_by("-total_points")
        return list(queryset).index(obj) + 1

    