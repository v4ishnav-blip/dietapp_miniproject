from django.shortcuts import render
from dietlense_app.models import *
from dietlense_app.serializers import *
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from dietlense_app.utility_funcs import *
from dietlense_app.permissions import IsOwner
# Create your views here.

class CreateUser(CreateAPIView):
    serializer_class=UserSerializer

class ProfileView(CreateAPIView):
    serializer_class=UserProfileSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        user_object=self.request.user
        # data=serializer.validated_data
        # bmr=calculate_bmr(
        #     age=data.get('age'),
        #     height=data.get('height'),
        #     weight=data.get('weight'),
        #     gender=data.get('gender'),
        #     activity_level=data.get('activity_level')

        # )
        return serializer.save(owner=user_object,bmr=user_object)

class profileRetrieveView(RetrieveAPIView,UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=UserProfileSerializer
    queryset=Userprofile.objects.all()

class UserRetrieveView(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=UserSerializer
    queryset=CustomUser.objects.all()


class FoodLogCreateView(CreateAPIView,ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

# class FoodlogList(ListAPIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsOwner]
#     serializer_class=FoodLogSerializer
#     queryset=FoodLog.objects.all()

class FoodlogRetriveView(RetrieveAPIView,DestroyAPIView,UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()



    