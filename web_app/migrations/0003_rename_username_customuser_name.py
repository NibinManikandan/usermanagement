# Generated by Django 4.2.6 on 2023-11-08 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_customuser_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='username',
            new_name='name',
        ),
    ]