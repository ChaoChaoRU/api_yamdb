from django.contrib.auth.models import AbstractUser
#from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

#user = get_user_model()
#moderator = get_user_model()
#admin = get_user_model()


class CustomUser(AbstractUser):
    class UserRole:
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
        CHOICES = [
            (USER, 'user'),
            (MODERATOR, 'moderator'),
            (ADMIN, 'admin'), 
        ]
#    CHOICES = (
#        user,
#        moderator,
#        admin,
#    )
    username = models.CharField(
        max_length=254,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        help_text='Введите email',
        unique=True
    )
    first_name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Введите имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=254,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Напишите кратко о себе',
        blank=True,
    )
    role = models.CharField(
        max_length=254,
        verbose_name='Статус пользователя',
        help_text='Введите статус пользователя',
        choices=UserRole.CHOICES,
        default=UserRole.USER,
    )

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR

    #is_staff = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', 
                            db_index=True, max_length=256)
    year = models.PositiveSmallIntegerField(blank=True, validators=[year_validator])
    description = models.TextField(default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


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
        related_name='reviews',
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
        verbose_name='Дата комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text