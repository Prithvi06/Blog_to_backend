from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import *
from .serializers import *
from .permissions import IsTokenValid
# Create your views here.


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
     
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'message':"Iinvalid Credentials"})


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def post(self,request):
        token = request.auth
        BlackListedToken.objects.filter(user=request.user).delete()
        BlackListedToken.objects.create(user=request.user, token=token)
        logout(request)
        return Response({'message':"User logout successful"})


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serialize_data = UserSerializer(data=request.data)
        if serialize_data.is_valid(raise_exception=True):
            serialize_data.save()
            return Response({"message": "User register successfully"}, status=status.HTTP_200_OK)


class BlogPostView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def get(self, request):
        post_data = BlogPost.objects.all()
        serializer_data = PostSerializer(post_data, many=True)
        return Response(serializer_data.data)

    def post(self, request):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data._mutable = False
        serialize_data = PostSerializer(data=request.data)
        if serialize_data.is_valid(raise_exception=True):
            serialize_data.save()
            return Response({"message": "Post created successfully"})


class BlogPostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def get(self, request, slug):
        post_data = BlogPost.objects.filter(slug=slug).first()
        serializer_data = PostSerializer(post_data)
        return Response(serializer_data.data)


class CommentView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def get(self, request, slug):
        comment_data = Comment.objects.filter(blogpost__slug=slug)
        serializer_data = CommentSerializer(comment_data, many=True)
        return Response(serializer_data.data)

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = False
        serialize_data = CommentSerializer(data=request.data)
        if serialize_data.is_valid(raise_exception=True):
            serialize_data.save()
            return Response({"message": "Comment post successfully"})


class ReplyView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = False
        serialize_data = ReplySerializer(data=request.data)
        if serialize_data.is_valid(raise_exception=True):
            serialize_data.save()
            return Response({"message": "Reply post successfully"})