# Generated by Django 4.1.5 on 2023-01-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panalyzer', '0003_picture_alter_exerciseselection_exercise_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklycheckins',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
