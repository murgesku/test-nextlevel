# Generated by Django 4.1.10 on 2023-08-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=18, verbose_name='Номер телефона')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Адрес электронной почты')),
            ],
            options={
                'verbose_name': 'Контакт записной книжки',
            },
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(models.F('first_name'), models.F('last_name'), name='unique_contact_name'),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(models.F('phone_number'), name='unique_contact_phone'),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(models.F('email'), name='unique_contact_email'),
        ),
    ]
