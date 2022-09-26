from dataclasses import field, fields
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "middle_name", "last_name", "image"]
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            image=validated_data.get("image")
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = "__all__"
        extra_kwargs = {
            'author': {'required': True},
            'title': {'required': True},
        }


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': True},
            'comment': {'required': True},
            'body': {'required': True},
        }
        

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id','user', 'blogpost', 'body', 'replies']
        extra_kwargs = {
            'user': {'required': True},
            'blogpost': {'required': True},
            'body': {'required': True},
        }
