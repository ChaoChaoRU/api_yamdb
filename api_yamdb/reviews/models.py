from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


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
    name = models.CharField
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


class Review(models.Model):
    text = models.CharField(
        max_length=2000,
        verbose_name='Ваш отзыв',
    )
    author = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name='Ваша оценка',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='Произведение',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
