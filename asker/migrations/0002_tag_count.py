# Generated by Django 2.1.7 on 2019-05-02 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]