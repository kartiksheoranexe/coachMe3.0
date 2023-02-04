import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import Http404

from django.shortcuts import get_object_or_404

from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from main.models import CustomUser, Coach, Certificate, Achievement, Package, Client, Mapping, Wallet, Transaction, ClientOnboard, Blog, Like, Comment, Share, Negotiate
from main.serializers import CustomUserSerializer, CoachSerializer, PackageSerializer, ClientSerializer, MappingSerializer, WalletSerializer, TransactionsSerializer, BlogSerializer, LikeSerializer, ShareSerializer, CommentSerializer, NegotiateUserSerializer, NegotiateCoachSerializer

class CustomUserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            Wallet.objects.create(user=user, balance=0, cm_tokens=0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Username, email, or phone number already in use"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        # Validate the login credentials
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            token = AuthToken.objects.create(user)
            return Response({'token': token[1]})
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    def post(self, request):
        # Get the user's JWT
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        t = token[:8]
        auth_token = AuthToken.objects.get(token_key=t)
        auth_token.delete()
        return Response({"User Logged Out Succesfully!!"}, status=status.HTTP_204_NO_CONTENT)


class CoachCreateAPIView(generics.CreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id
        request.data['years_of_experience'] = self.request.data.get(
            'years_of_experience')
        request.data['category'] = self.request.data.get('category')
        request.data['coach_subtype'] = self.request.data.get('coach_subtype')
        achievement_titles = request.data.get('achievement_titles', [])
        certificate_titles = request.data.get('certificate_titles', [])

        achievements = []
        certificates = []
        for title in achievement_titles:
            achievement = Achievement.objects.create(title=title)
            achievements.append(achievement)
        for title in certificate_titles:
            certificate = Certificate.objects.create(title=title)
            certificates.append(certificate)

        request.data['achievements'] = [a.pk for a in achievements]
        request.data['certifications'] = [c.pk for c in certificates]

        if user.user_type == 'C':
            raise ValidationError({'error': 'User is already a coach'})

        user.user_type = 'C'
        user.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CoachListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        coaches = Coach.objects.all()
        category = request.query_params.get('category', None)
        subcategory = request.query_params.get('subcategory', None)

        if category:
            coaches = coaches.filter(category=category)

        if subcategory:
            coaches = coaches.filter(coach_subtype=subcategory)

        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)


class PackageCreateAPIView(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        coach_id = self.kwargs['coach_id']
        coach = get_object_or_404(Coach, pk=coach_id)
        serializer.save(coach=coach)


class CoachPackagesListAPIView(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        coach_id = self.kwargs['coach_id']
        coach_obj = get_object_or_404(Coach, pk=coach_id)
        return Package.objects.filter(coach=coach_obj)


class ClientCreateAPIView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        package_id = self.kwargs['package_id']
        package = get_object_or_404(Package, pk=package_id)
        user = self.request.user
        wallet, created = Wallet.objects.get_or_create(user=user)
        package_obj = Package.objects.get(id=package_id)
        negotiate_obj = Negotiate.objects.get(package=package_obj, status='S')
        latest_price = negotiate_obj.updated_price
        

        if wallet.balance >= latest_price:
            wallet.balance -= latest_price
            wallet.save()

            end_date = datetime.now()
            if package.duration_type == 'Y':
                end_date += relativedelta(years=package.duration)
            elif package.duration_type == 'M':
                end_date += relativedelta(months=package.duration)
            elif package.duration_type == 'D':
                end_date += relativedelta(days=package.duration)

            client = serializer.save(coach=package.coach, user=user)

            Mapping.objects.create(package_id=package, coach_id=package.coach,
                                   client=client, start_date=datetime.now(), end_date=end_date, actual_price=latest_price)

            Transaction.objects.create(wallet=wallet, amount_paid=latest_price, transaction_status='S',
                                       transaction_mode='UPI', transaction_type='P', remark='Package purchase', client=client)

            user.user_type = 'L'
            user.save()
        else:
            raise ValidationError({'error': 'Insufficient balance'})

class NegotiateCreateView(generics.CreateAPIView):
    queryset = Negotiate.objects.all()
    serializer_class = NegotiateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        package_id = self.request.data.get('package')
        user_id = self.request.data.get('client')
        package = Package.objects.get(id=package_id)
        user = CustomUser.objects.get(id=user_id)
        coach = package.coach
        updated_price = package.base_price
        data = {}
        negotiate_message_client = self.request.data.get('negotiate_message_client')
        negotiate_price_client = self.request.data.get('negotiate_price_client')
        negotiate = serializer.save(package=package, client=user, updated_price=updated_price, negotiate_message_client=negotiate_message_client, negotiate_price_client=negotiate_price_client)
        # data = {
        #     "negotiate_id": negotiate.id,
        #     "coach_id": coach.id,
        #     "status": negotiate.status
        # }
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CoachNegotiateCreatView(generics.CreateAPIView):
    queryset = Negotiate.objects.all()
    serializer_class = NegotiateCoachSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        negotiate_id = self.request.data.get('negotiate_id')
        negotiate = Negotiate.objects.get(id=negotiate_id)
        package = negotiate.package
        client = negotiate.client
        coach = package.coach
        updated_price = negotiate.updated_price
        data = {}
        negotiate_message_coach = self.request.data.get('negotiate_message_coach')
        negotiate_price_coach = self.request.data.get('negotiate_price_coach')

        negotiate.negotiate_message_coach = negotiate_message_coach
        negotiate.negotiate_price_coach = negotiate_price_coach
        negotiate.updated_price = negotiate_price_coach

        if negotiate.negotiate_price_client == negotiate.negotiate_price_coach:
            negotiate.status = 'S'
        else:
            negotiate.status = 'P'
        negotiate.save()
        
        data = {
            "negotiate_id": negotiate.id,
            "status": negotiate.status,
            "updated_price": negotiate.updated_price
        }
        return JsonResponse({"Data": data}, status=status.HTTP_200_OK)



class MappingListAPIView(generics.ListAPIView):
    serializer_class = MappingSerializer

    def get_queryset(self):
        coach_id = self.kwargs['coach_id']
        return Mapping.objects.filter(coach_id=coach_id)


class WalletDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Wallet, user=user)


class TransactionListAPIView(generics.ListAPIView):

    serializer_class = TransactionsSerializer

    def get_queryset(self):
        user = self.request.user
        wallet, created = Wallet.objects.get_or_create(user=user)
        return Transaction.objects.filter(wallet=wallet)


class ClientOnboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        coach = request.user
        coach_obj = Coach.objects.filter(user=coach).first()
        client_id = request.data.get('client_id')
        data = request.data.get('data')

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            return Response({"error": "Invalid client_id"}, status=status.HTTP_400_BAD_REQUEST)

        ClientOnboard.objects.create(coach=coach_obj, client=client, data=data)

        return Response({"success": "Client onboarding data saved successfully"}, status=status.HTTP_201_CREATED)


class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.user_type != 'C':
            raise PermissionDenied(detail='User is not a coach')
        coach = Coach.objects.get(user=user)
        request.data['coach'] = coach.id
        request.data['title'] = self.request.data.get('title')
        request.data['content'] = self.request.data.get('content')
        request.data['image'] = self.request.data.get('image')
        request.data['video'] = self.request.data.get('video')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        blog = Blog.objects.get(id=request.data['blog'])
        total_likes = blog.likes.count()
        users_who_liked = CustomUser.objects.filter(likes__blog=blog)
        user_list = []
        for user in users_who_liked:
            user_list.append(user.username)
        return Response({'total_likes': total_likes, 'users_who_liked': user_list}, status=status.HTTP_201_CREATED, headers=headers)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        blog_id = self.request.data.get('blog')
        queryset = Comment.objects.filter(blog=blog_id)
        return queryset

class ShareCreateView(generics.CreateAPIView):
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        blog_id = request.data['blog']
        blog_obj = Blog.objects.get(id=blog_id)
        recipient_usernames = request.data.get('recipients')
        if not recipient_usernames or len(recipient_usernames) > 5:
            raise ValidationError({'error': 'Please provide up to 5 recipients'})
        recipients = CustomUser.objects.filter(username__in=recipient_usernames)
        share = Share.objects.create(user=user, blog=blog_obj)
        share.recipients.set(recipients)
        share.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


