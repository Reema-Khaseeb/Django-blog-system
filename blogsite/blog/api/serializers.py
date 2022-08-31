"""Serializers for blog app models"""
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    """Serialize user model"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', )

class PostSerializer(serializers.ModelSerializer):
    """Serialize post model"""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'status',
            'author',
        )

class CommentSerializer(serializers.ModelSerializer):
    """Serialize comment model"""
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'post', )
