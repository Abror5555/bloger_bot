# Generated by Django 5.0.2 on 2024-03-03 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_bloger_user_alter_user_bloger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='main.user', unique=True),
        ),
    ]
