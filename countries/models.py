from django.db import models


# this models holds all the countries in which DriverHealth operates.
class Country(models.Model):
    long_name = models.CharField(max_length=150, blank=False)
    short_name = models.CharField(max_length=10, blank=True)
    general_coordinates = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = ('Countries')

    def __str__(self):
        return self.long_name

