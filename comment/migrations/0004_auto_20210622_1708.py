# Generated by Django 3.1.3 on 2021-06-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment_prediction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='prediction',
            field=models.BooleanField(default=True),
        ),
    ]
