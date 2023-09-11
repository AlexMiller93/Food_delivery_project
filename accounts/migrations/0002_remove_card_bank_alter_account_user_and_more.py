# Generated by Django 4.2.4 on 2023-08-28 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='bank',
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_type',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Manager', 'Manager'), ('Courier', 'Courier'), ('Cook', 'Cook')], default='Customer', max_length=8),
        ),
    ]