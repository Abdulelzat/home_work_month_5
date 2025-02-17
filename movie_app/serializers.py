from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movie_count'.split()

    def get_movie_count(self, director):
        return director.movies.count()


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()
        depth = 2

    def get_rating(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum([review.stars for review in reviews])
            rating = sum_reviews / len(reviews)
            return rating
        else:
            return None


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=1)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=1)
    description = serializers.CharField(required=True, max_length=255, min_length=1)
    duration = serializers.IntegerField(required=True)
    director_id = serializers.IntegerField(required=True, min_value=1)

    # def validate(self, attrs):
    #     try:
    #         Movie.objects.get(id=attrs['director_id'])
    #     except Movie.DoesNotExist:
    #         raise ValidationError('Movie does not exist')
    #     return attrs

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist')
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, max_length=255, min_length=1)
    stars = serializers.IntegerField(required=True, min_value=1)
    movie_id = serializers.IntegerField(required=True, min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            Director.objects.get(id=movie_id)
        except:
            raise ValidationError('Director does not exist')
        return movie_id