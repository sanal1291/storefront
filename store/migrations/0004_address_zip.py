# Generated by Django 3.2.7 on 2021-09-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_slug_to_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
