# Generated by Django 4.1.5 on 2023-02-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0002_alter_fooditem_serving_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='serving_type',
            field=models.CharField(choices=[('ounce', 'Ounce'), ('gram', 'Gram'), ('pound', 'Pound'), ('kilogram', 'Kilogram'), ('pinch', 'Pinch'), ('liter', 'Liter'), ('fluid ounce', 'Fluid ounce'), ('gallon', 'Gallon'), ('pint', 'Pint'), ('quart', 'Quart'), ('milliliter', 'Milliliter'), ('drop', 'Drop'), ('cup', 'Cup'), ('tablespoon', 'Tablespoon'), ('teaspoon', 'Teaspoon')], max_length=20),
        ),
    ]
