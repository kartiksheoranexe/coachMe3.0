# Generated by Django 4.1.5 on 2023-01-07 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_rename_data_clientonboard_client_onboarddata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientonboard',
            old_name='client_onboarddata',
            new_name='client_onboard_data',
        ),
    ]
