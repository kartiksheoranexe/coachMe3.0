# Generated by Django 4.1.5 on 2023-01-07 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_avatar', models.ImageField(blank=True, null=True, upload_to='clientavatars/')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.coach')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
