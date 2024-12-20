# Generated by Django 5.0.7 on 2024-11-16 03:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('promise', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('color', models.CharField(choices=[('#FF6A3B', 'Orange'), ('#4076BA', 'Blue'), ('#C04277', 'Pink'), ('#16857A', 'Green'), ('#A97C50', 'Brown')], default='#FF6A3B', max_length=7)),
                ('is_public', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('memo', models.TextField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='plan.category')),
                ('participant', models.ManyToManyField(blank=True, related_name='participating_plan', to=settings.AUTH_USER_MODEL)),
                ('promise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promise_creates_this_plan', to='promise.promise')),
            ],
        ),
        migrations.CreateModel(
            name='PlanCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.category')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
            ],
        ),
    ]
