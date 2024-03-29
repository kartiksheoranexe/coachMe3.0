from rest_framework import serializers

from main.models import CustomUser, Coach, Achievement, Certificate, Package, Client, Mapping, Wallet, Transaction, Blog, Comment, Like, Share, Negotiate
from main.models import COACH_TYPE_CHOICES, FITNESS_CHOICES


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password',
                  'dob', 'gender', 'user_type', 'phone_no']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CoachSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    achievements = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Achievement.objects.all())
    certifications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Certificate.objects.all())
    category = serializers.ChoiceField(choices=COACH_TYPE_CHOICES)
    coach_subtype = serializers.ChoiceField(choices=FITNESS_CHOICES)

    class Meta:
        model = Coach
        fields = ('id', 'user', 'username', 'bio', 'years_of_experience', 'certifications',
                  'achievements', 'is_active', 'coach_avatar', 'rating', 'website', 'status', 'category', 'coach_subtype')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'coach', 'package_name', 'package_desc',
                  'duration_type', 'duration', 'base_price')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'coach', 'client_avatar']


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        fields = ['id', 'package_id', 'coach_id',
                  'client', 'start_date', 'end_date']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', 'cm_tokens')


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('unique_id', 'amount_paid', 'transaction_status',
                  'transaction_mode', 'transaction_date', 'transaction_type', 'remark')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'coach', 'created_at', 'image', 'video')

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Like
        fields = ('id', 'user', 'username', 'blog', 'created_at')

class ShareSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Share
        fields = ('id', 'username', 'blog', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'blog', 'comment_text', 'created_at')

class NegotiateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiate
        fields = ('id', 'package', 'client', 'negotiate_message_client', 'negotiate_price_client', 'updated_price', 'status')

class NegotiateCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiate
        fields = ('id', 'negotiate_message_coach', 'negotiate_price_coach', 'updated_price', 'status')
