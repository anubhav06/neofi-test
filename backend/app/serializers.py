from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, SharedNote


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = '__all__'
