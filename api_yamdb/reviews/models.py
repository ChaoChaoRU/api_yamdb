from django.db import models
from .validators import year_validator
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomerUser(AbstractUser):
    email = models.EmailField(
        max_length=200,
        verbose_name='Адрес электронной почты',
        help_text='Введите email',
        unique=True
    )
    role = models.CharField(
        max_length=200,
        verbose_name='Статус пользователя',
        help_text='Введите статус пользователя'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id', ]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(db_index=True, max_length=256)
    year = models.IntegerField(blank=True, validators=[year_validator])
    description = models.TextField
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)

    class Meta:
        ordering = ['-id', ]
