# Generated by Django 4.1.5 on 2023-01-06 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_customuser_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=254)),
                ('thumbnail', models.ImageField(upload_to='achievements/')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=254)),
                ('thumbnail', models.ImageField(upload_to='certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=254)),
                ('years_of_experience', models.FloatField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('coach_avatar', models.ImageField(blank=True, null=True, upload_to='coachavatars/')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Available'), ('W', 'Away'), ('O', 'Offline'), ('V', 'On vacation')], max_length=20)),
                ('achievements', models.ManyToManyField(to='main.achievement')),
                ('certifications', models.ManyToManyField(to='main.certificate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
