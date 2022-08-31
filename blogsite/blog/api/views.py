"""
Blog API views
"""
from django.utils import timezone

from rest_framework import generics
from rest_framework import permissions

from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from ..models import Post, Comment


class PostListCreateView(generics.ListCreateAPIView):
    """Get list of posts and create new one just for authenticated users"""
    serializer_class = PostSerializer
    queryset = Post.published_objects.filter(published_at__lte=timezone.now())
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Get post detail and adjust it, it's authorized just for the author of the post"""
    serializer_class = PostSerializer
    queryset = Post.published_objects.filter(published_at__lte=timezone.now())
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """Get list of comments and create new one"""
    serializer_class = CommentSerializer
    queryset = Comment.active_objects.all()


class CommentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """All users can get comment detail and update it"""
    serializer_class = CommentSerializer
    queryset = Comment.active_objects.all()
