from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserLoginSerializer, SMSCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import SMSCode


class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_active=False
        )

        code = "".join([str(random.randint(0, 9)) for i in range(6)])
        SMSCode.objects.create(user=user, sms_code=code)

        send_mail(
            'Your code',
            message=f'Your confirmation code is: {code}',
            from_email='no-reply@example.com',
            recipient_list=[user.email]
        )

        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid user or password'})


class ConfirmSMSAPIView(APIView):
    def post(self, request):
        serializer = SMSCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sms_code = serializer.validated_data.get('SMS')

        try:
            sms = SMSCode.objects.get(sms_code=sms_code)
        except SMSCode.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Code is invalid'})

        sms.user.is_active = True
        sms.user.save()
        sms.delete()

        return Response(data={'active': True}, status=status.HTTP_200_OK)
