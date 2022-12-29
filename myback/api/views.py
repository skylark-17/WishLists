from .serializers import *
from .models import *
from rest_framework import generics

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from .serializers import *
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken

class WishList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        post = Wish.objects.all()
        serializer = WishSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CreateWish(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        wish = Wish.objects.create(
            title=request.data.get("title"),
            text=request.data.get("text"),
            nickname=request.data.get("nickname"),
        )
        return Response(status=HTTP_200_OK)


class WishListAll(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishSerializer
    queryset = Wish.objects.all()

class WishCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishSerializer

class WishDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishSerializer
    queryset = Wish.objects.all()


class CreateUser(APIView):
    def post(self, request):
        if User.objects.filter(username=request.data.get("username")).count():
            return Response(status=HTTP_403_FORBIDDEN)

        user = User.objects.create_user(
            username=request.data.get("username"),
            email=request.data.get("email"),
            password=request.data.get("password"))

        refresh = RefreshToken.for_user(user=user)
        access = refresh.access_token
        return Response({
            "access": str(access),
            "refresh": str(refresh)
            }, status=HTTP_200_OK)


class GetWishesByUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        nickname = request.data
        return JsonResponse(list(Wish.objects.filter(nickname=nickname).values()), safe=False)

class DeleteWish(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        id = request.data
        Wish.objects.filter(id=id).delete()
        return Response(status=HTTP_200_OK)

