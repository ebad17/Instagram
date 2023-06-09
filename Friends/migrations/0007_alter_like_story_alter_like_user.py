# Generated by Django 4.2 on 2023-05-08 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Friends', '0006_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='story',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to='Friends.story'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
