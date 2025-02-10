from rest_framework import serializers
from movie_app.models import Director, Movie, Review


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