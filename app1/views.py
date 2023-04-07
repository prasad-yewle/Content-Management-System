from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from .models import CustomUser, Content
from .serializers import CustomUserSerializer, ContentSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthor(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to perform certain actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_staff

#Code for registration
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

#Code for author to post content
class ContentCreateView(generics.CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Code for Token 
class CustomTokenObtainPairView(generics.CreateAPIView):
    serializer_class = CustomTokenObtainPairSerializer

class ContentListView(generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()
        else:
            return Content.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Code to view content
class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()
        else:
            return Content.objects.filter(author=self.request.user)

#Code to update content     
class ContentUpdateView(generics.UpdateAPIView):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated & (IsAuthor | IsAdmin)]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Content.objects.all()
        else:
            queryset = Content.objects.filter(author=user)
        return queryset

#Code to delete content  
class ContentDeleteView(APIView):
    permission_classes = [IsAuthenticated & (IsAuthor | IsAdmin)]

    def delete(self, request, pk):
        try:
            content = Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is author of the content or admin
        if not request.user.is_staff and request.user != content.author:
            return Response({"message": "Unauthorized to delete the content"}, status=status.HTTP_401_UNAUTHORIZED)

        content.delete()
        return Response({"message": "Content deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#Code to search data from content
class ContentSearchView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.AllowAny] # allow any user to access this endpoint

    def get_queryset(self):
        query = self.request.GET.get('q') # retrieve search query from request parameters
        queryset = Content.objects.all() # start with all content objects

        if query: # if query is not empty
            # search for matching terms in title, body, summary fields using Q objects
            queryset = queryset.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(summary__icontains=query))

        return queryset
