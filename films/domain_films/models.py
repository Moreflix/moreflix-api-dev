from django.db import models

class Film(models.Model):
    source = models.CharField(max_length=1000, blank= False, null= False)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    sinopsis = models.TextField()
    year = models.IntegerField()
    rating = models.FloatField()
    genre = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    studio = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'film'
        managed = True
        verbose_name = 'Film'
        verbose_name_plural = 'Films'

    def __str__(self):
        return f"{self.title} {self.year}"

