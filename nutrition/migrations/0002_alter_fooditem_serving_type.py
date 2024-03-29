# Generated by Django 4.1.5 on 2023-02-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='serving_type',
            field=models.CharField(choices=[('Ounce', 'Ounce'), ('Gram', 'Gram'), ('Pound', 'Pound'), ('Kilogram', 'Kilogram'), ('Pinch', 'Pinch'), ('Liter', 'Liter'), ('Fluid ounce', 'Fluid ounce'), ('Gallon', 'Gallon'), ('Pint', 'Pint'), ('Quart', 'Quart'), ('Milliliter', 'Milliliter'), ('Drop', 'Drop'), ('Cup', 'Cup'), ('Tablespoon', 'Tablespoon'), ('Teaspoon', 'Teaspoon')], max_length=20),
        ),
    ]
