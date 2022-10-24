from django.db import models
from django.utils import timezone



class Gallery_image(models.Model):
    IMAGE_CATEGORY = [
        (1, 'Driving Test Image'),
        (2, 'Promotions')
    ]
    image = models.ImageField(upload_to='Gallery_Images/', blank=False)
    image_type = models.SmallIntegerField(default=1, choices=IMAGE_CATEGORY)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return f'{self.date_created}'
