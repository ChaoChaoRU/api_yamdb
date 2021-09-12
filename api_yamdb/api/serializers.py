from rest_framework import serializers

from reviews.models import CustomUser, Genre, Title, Category


class GetUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ('username',)
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )


class GetPatchDeteleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ('username',)
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role', )


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