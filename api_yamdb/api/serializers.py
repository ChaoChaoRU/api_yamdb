from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


User = get_user_model()



'''class GetUsersSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = CustomUser
#        fields = (
#            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )
#class CreateUserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = CustomUser
#        fields = (
#            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )
#class GetPatchDeteleUserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = CustomUser
#        fields = (
#            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )'''


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Вы не можете оставлять больше одного отзыва.'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('username', 'role', 'email')
        model = CustomUser


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CustomUser
        read_only_fields = ('role',)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('You can not use this username.')
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()