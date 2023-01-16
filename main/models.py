import uuid
from jsonfield import JSONField

from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.db import models

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

USER_TYPE_CHOICES = [
    ('U', 'User'),
    ('C', 'Coach'),
    ('L', 'Client'),
]

COACH_STATUS_CHOICES = [
    ('A', 'Available'),
    ('W', 'Away'),
    ('O', 'Offline'),
    ('V', 'On vacation'),
]

DURATION_TYPE = (
    ('Y', 'Years'),
    ('M',  'Months'),
    ('D',  'Days')
)

STATUS = (
    ('P', 'Pending'),
    ('S',  'Success'),
    ('C',  'Cancelled')
)

MODE = (
    ('CC', 'Credit Card'),
    ('DC',  'Debit Card'),
    ('UPI',  'UPI'),
    ('ND', 'Not Defined')
)

TYPE = (
    ('P', 'Purchase'),
    ('R', 'Reverse'),
)

COACH_TYPE_CHOICES = (
    ('F', 'Fitness'),
    ('L', 'Life Coaching'),
    ('B', 'Business Coaching'),
    ('E', 'Executive Coaching'),
    ('H', 'Health and Wellness Coaching'),
    ('S', 'Spiritual Coaching'),
    ('A', 'Athletic Coaching'),
    ('C', 'Career Coaching'),
)

LIFESTYLE_CHOICES = (
    ('LS', 'Lifestyle Coaching'),
    ('PD', 'Personality Development Coaching'),
    ('RC', 'Relationship Coaching'),
    ('TM', 'Time Management Coaching'),
)
FITNESS_CHOICES = (
    ('BB', 'Body Building'),
    ('SF', 'Strength and Fitness'),
    ('PL', 'Powerlifting'),
)
BUSINESS_CHOICES = (
    ('LD', 'Leadership Coaching'),
    ('SL', 'Sales Coaching'),
    ('MR', 'Marketing Coaching'),
)

EXECUTIVE_CHOICES = (
    ('CE', 'CEO Coaching'),
    ('BR', 'Board Director Coaching'),
)

HEALTH_N_WELLNESS_CHOICES = (
    ('MH', 'Mental Health Coaching'),
    ('NT', 'Nutrition Coaching'),
    ('SM', 'Stress Management Coaching'),
)

SPIRITUAL_CHOICES = (
    ('MD', 'Meditation coaching'),
    ('MF', 'Mindfulness coaching'),
    ('IS', 'Interfaith/inter-spiritual coaching'),
)

ATHLETIC_CHOICES = (
    ('FB', 'Football coaching'),
    ('CH', 'Chess coaching'),
    ('BX', 'Boxing coaching'),
)

CAREER_CHOICES = (
    ('RW', 'Resume Writing coaching'),
    ('IV', 'Interview coaching'),
    ('JS', 'Job Search coaching'),
)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    phone_no = PhoneField(help_text='Contact phone number', unique=True)


class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to='achievements/')

    def __str__(self):
        return self.title


class Coach(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=254)
    category = models.CharField(
        max_length=1, choices=COACH_TYPE_CHOICES, default='F',)
    coach_subtype = models.CharField(
        max_length=2, choices=FITNESS_CHOICES, default='BB',)
    years_of_experience = models.FloatField(null=True, blank=True)
    certifications = models.ManyToManyField(Certificate)
    achievements = models.ManyToManyField(Achievement)
    is_active = models.BooleanField(('active'), default=True)
    coach_avatar = models.ImageField(
        upload_to='coachavatars/', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=COACH_STATUS_CHOICES)

    def __str__(self):
        return self.user.username


class Package(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    package_desc = models.CharField(max_length=254)
    duration_type = models.CharField(max_length=1, choices=DURATION_TYPE)
    duration = models.IntegerField()
    base_price = models.IntegerField()

    def __str__(self):
        return self.package_name


class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    client_avatar = models.ImageField(
        upload_to='clientavatars/', null=True, blank=True)
    channel_id = models.CharField(
        max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Negotiate(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    negotiate_message_coach = models.CharField(max_length=255)
    negotiate_message_client = models.CharField(max_length=255)
    negotiate_price_coach = models.IntegerField(default=0)
    negotiate_price_client = models.IntegerField(default=0)
    updated_price = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")

class Mapping(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    coach_id = models.ForeignKey(Coach, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    actual_price = models.IntegerField(default=0)


class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    cm_tokens = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    unique_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    amount_paid = models.IntegerField()
    transaction_status = models.CharField(max_length=1, choices=STATUS)
    transaction_mode = models.CharField(max_length=3, choices=MODE)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(max_length=1, choices=TYPE)
    remark = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.unique_id)


class ClientOnboard(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_onboard_data = JSONField()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    coach = models.ForeignKey(
        Coach, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blogs/images/', blank=True, null=True)
    video = models.FileField(upload_to='blogs/videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Share(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='shares')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(CustomUser, related_name='shares_received')


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
