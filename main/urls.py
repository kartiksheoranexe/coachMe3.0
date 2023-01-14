from django.urls import path

from . import views
from main.parseexcelonboard import parse_excel_file
from main.slackcom import communicate
from main.sendemailonboard import SendEmailAPIView
from main.views import CustomUserCreateAPIView, LoginAPIView, LogoutAPIView, CoachCreateAPIView, CoachListAPIView, PackageCreateAPIView, CoachPackagesListAPIView, ClientCreateAPIView, MappingListAPIView, WalletDetailAPIView, TransactionListAPIView, ClientOnboardAPIView

urlpatterns = [
    path('register-user/', CustomUserCreateAPIView.as_view(), name='register'),
    path('login-user/', LoginAPIView.as_view(), name='login'),
    path('logout-user/', LogoutAPIView.as_view(), name='logout'),

    path('register-as-coach/', CoachCreateAPIView.as_view(),
         name='coach-registeration'),
    path('coaches/', CoachListAPIView.as_view(), name='coach-list'),
    path('add-package/create/<int:coach_id>/',
         PackageCreateAPIView.as_view(), name='create-package'),
    path('coaches/<int:coach_id>/packages-list/',
         CoachPackagesListAPIView.as_view(), name='coach-packages-list'),
    path('mappings/<int:coach_id>/',
         MappingListAPIView.as_view(), name='mapping-list'),

    path('coaches/<int:coach_id>/packages/<int:package_id>/create-client/',
         ClientCreateAPIView.as_view(), name='create-client'),

    path('balance/', WalletDetailAPIView.as_view(), name='balance'),
    path('transactions/', TransactionListAPIView.as_view(), name='transactions'),

    path('client-onboard/', views.ClientOnboardAPIView.as_view(),
         name='client-onboard'),

    path('parse-client-onboard/', parse_excel_file,
         name='parse-client-onboard'),

    path('sendonboardfilemail/', SendEmailAPIView.as_view()),

    path("slack-comm/", communicate, name="send_message"),


]
