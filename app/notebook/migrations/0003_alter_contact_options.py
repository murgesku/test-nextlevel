# Generated by Django 4.1.10 on 2023-08-26 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0002_data_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['id'], 'verbose_name': 'Контакт записной книжки'},
        ),
    ]