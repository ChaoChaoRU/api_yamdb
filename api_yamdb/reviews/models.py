from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class CustomUser(AbstractBaseUser):

    USERNAME_FIELD = ['username']
    REQUIRED_FIELDS = ['first_name']

    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    CHOICES = (
        (user, 'Пользователь'),
        (moderator, 'Модератор'),
        (admin, 'Администратор'),
    )
    username = models.CharField(
        max_length=256,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        help_text='Введите email',
        unique=True
    )
    first_name = models.CharField(
        max_length=256,
        verbose_name='Имя',
        help_text='Введите имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=256,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Напишите кратко о себе',
        blank=True,
    )
    role = models.CharField(
        max_length=40,
        verbose_name='Статус пользователя',
        help_text='Введите статус пользователя',
        choices=CHOICES,
        default=user,
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # user_permissions = models.BooleanField(default=False)
    # groups
    # is_active

    def __str__(self):
        return self.username


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


class Review(models.Model):
    text = models.CharField(
        max_length=2000,
        verbose_name='Ваш отзыв',
    )
    author = models.ForeignKey(
        CustomUser,
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
        CustomUser,
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
