# Generated by Django 3.2.6 on 2021-08-27 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_chatlog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chatlog',
        ),
        migrations.AddField(
            model_name='contract',
            name='chats',
            field=models.TextField(default='채팅로그가 등록되지 않았습니다.'),
        ),
    ]
