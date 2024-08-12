# Generated by Django 4.2.7 on 2024-08-11 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('azureai', '0003_story_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='images',
        ),
        migrations.AddField(
            model_name='image',
            name='story',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='azureai.story'),
        ),
    ]
