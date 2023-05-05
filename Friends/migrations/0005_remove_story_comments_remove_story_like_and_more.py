# Generated by Django 4.2 on 2023-05-05 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Friends', '0004_remove_like_story_remove_like_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='story',
            name='like',
        ),
        migrations.RemoveField(
            model_name='story',
            name='reply',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to='Friends.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_reply', to='Friends.comment')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Friends.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]