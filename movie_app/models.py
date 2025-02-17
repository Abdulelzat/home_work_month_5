from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")

    def __str__(self):
        return self.title


class Review(models.Model):
    STARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    stars = models.PositiveIntegerField(choices=STARS, null=True, blank=True)



    def __str__(self):
        return f"Review for {self.movie.title}"