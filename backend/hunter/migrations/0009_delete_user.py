# Generated by Django 4.1.7 on 2023-03-10 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0008_user_username_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
