from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=18, verbose_name="Номер телефона")
    email = models.CharField(max_length=100, null=True, verbose_name="Адрес электронной почты")

    class Meta:
        verbose_name = "Контакт записной книжки"
        ordering = ['id']
        constraints = [
            models.UniqueConstraint('first_name', 'last_name', name='unique_contact_name'),
            models.UniqueConstraint('phone_number', name='unique_contact_phone'),
            models.UniqueConstraint('email', name='unique_contact_email'),
        ]


__all__ = ('Contact',)
