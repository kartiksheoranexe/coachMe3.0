from django.contrib import admin
from main.models import CustomUser, Coach, Achievement, Certificate, Package, Client, Mapping, Wallet, Transaction, ClientOnboard

# Register your models here.


class MappingAdmin(admin.ModelAdmin):
    list_display = ['package_id', 'coach_id',
                    'client', 'start_date', 'end_date']


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_type', 'phone_no', 'dob', 'gender']


class CoachAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'coach_subtype', 'rating']


class PackageAdmin(admin.ModelAdmin):
    list_display = ['coach', 'duration_type', 'duration', 'base_price']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'coach']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'cm_tokens']


class ClientOnboardAdmin(admin.ModelAdmin):
    list_display = ['coach', 'client']


admin.site.register(CustomUser, CustomUserAdmin),
admin.site.register(Coach, CoachAdmin),
admin.site.register(Achievement),
admin.site.register(Certificate),
admin.site.register(Package, PackageAdmin),
admin.site.register(Client, ClientAdmin),
admin.site.register(Mapping, MappingAdmin),
admin.site.register(Wallet, WalletAdmin),
admin.site.register(Transaction),
admin.site.register(ClientOnboard, ClientOnboardAdmin)
