# Generated by Django 5.2 on 2025-04-29 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_perfume_delivery_location_perfume_delivery_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfume',
            name='instagram_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perfume',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='perfume',
            name='tiktok_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perfume',
            name='whatsapp_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
