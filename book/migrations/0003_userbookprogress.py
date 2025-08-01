# Generated by Django 5.1.7 on 2025-06-01 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_chapter_options_chapter_chapter_num'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('reading', 'Reading'), ('completed', 'Completed'), ('dropped', 'Dropped'), ('plan_to_read', 'Plan to Read'), ('on_hold', 'On Hold')], default='plan_to_read', max_length=32)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='book.book')),
                ('last_read_chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_read_by_users', to='book.chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'book')},
            },
        ),
    ]
