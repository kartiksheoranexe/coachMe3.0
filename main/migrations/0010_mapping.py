# Generated by Django 4.1.5 on 2023-01-07 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_customuser_dob_alter_customuser_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client')),
                ('coach_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.coach')),
                ('package_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.package')),
            ],
        ),
    ]
